// -*- C++ -*-
//
// Prefetcher "stream buffer" data storage, managed as a group of co-operating
// stream buffers.
//
// Jeff Brown
// $Id: prefetch-streambuf.h,v 1.1.2.6 2008/11/26 21:39:32 jbrown Exp $
//

#ifndef PREFETCH_STREAMBUF_H
#define PREFETCH_STREAMBUF_H

#ifdef __cplusplus
extern "C" {
#endif

// XXX Note: as originally implemented, this allows for concurrent use by
// competing threads.  However, no explicit inter-thread priority or fairness
// is attempted; streams from different threads compete directly based on
// their local priority counters.

// Relevant papers to consider:
//
// Predictor-Directed Stream Buffers; Timothy Sherwood, Suleyman Sair,
// Brad Calder; MICRO 2000
//
// Memory-System Design Considerations for Dynamically-Scheduled Processors;
// Keith I. Farkas, Paul Chow, Norman P. Jouppi, Zvonko Vranesic; ISCA 1997
//
// Complexity/Performance Tradeoffs with Non-Blocking Loads; Keith Farkas,
// Norman Jouppi; ISCA 1994
//
// Evaluating Stream Buffers as Secondary Cache Replacement;
// S. Palacharla, R. Kessler; ISCA 1994


// Defined elsewhere
struct CoreResources;
struct CallbackQueue;


// (We're explicit with the "PF"/prefetch in the name, to avoid confusion
// with C++'s own <streambuf>.)
typedef struct PFStreamGroup PFStreamGroup;
typedef struct PFStreamExported PFStreamExported;


// time_queue is used to schedule internal callbacks that trigger prefetching,
// handle aging/maintenance, etc.
PFStreamGroup *pfsg_create(const char *id, const char *config_path,
                           struct CoreResources *parent_core,
                           struct CallbackQueue *time_queue,
                           int block_bytes);
void pfsg_destroy(PFStreamGroup *sg); 


// "Consumer" interface, looks something like a passive cache: consult
// stream buffer on cache misses, report misses for consideration.

// Search for data, presumably on an L1 miss.  returns nonzero iff usable data
// is found, and has sufficient permission to service the miss.
// On a hit, If allowed_access_type_ret is non-null, the "strongest" access
// permission conferred by the copy of the data in the streambuf is written
// there.  (Cache_Write would imply dirty data, but isn't used here.)
//
// This may invalidate an internal copy of the block, whether or not a hit is
// returned.  (cache_access_type is a CacheAccessType enum.)
// (addr_offset: offset from base_addr of the memory access)
int pfsg_cache_miss(PFStreamGroup *sg, LongAddr base_addr, int addr_offset,
                    int cache_access_type, mem_addr pc,
                    int *allowed_access_type_ret);

// Non-modifying probe
int pfsg_access_ok(const PFStreamGroup *sg, LongAddr base_addr,
                   int cache_access_type);

// Report mem-inst commits (for predictor/allocator training)
void pfsg_mem_commit(PFStreamGroup *sg, mem_addr pc, LongAddr va,
                     int was_write, int was_miss);

// Yield all copies of the given block for coherence reasons: downgrade them
// to "shared" status (i.e. revoke write permission), or optionally invalidate
// them altogether.
void pfsg_coher_yield(PFStreamGroup *sg, LongAddr base_addr, int invalidate);

// Signal the streambuf that its peer cache is evicting a modified block.
// (This is needed since the streambuf could have independently fetched a
// clean+exclusive copy of the data, since it's in the same "coherence domain"
// as the cache from the perspective of the coher. system.  That's OK, as long
// as we don't allow that stale data to ever be used to service a future
// access.  We could have the streambuf probe the cache before
// prefetching(ew), we could do explicit full coherence among on-core
// structures (ow), but it should suffice to just invalidate any stale copies
// on the comparatively rare evict events, which would precede that newer data
// becoming visible to the outside anyway.
void pfsg_cache_dirty_evict(PFStreamGroup *sg, LongAddr base_addr);

// Tell the streambuf to stop generating predictions and prefetches for the
// address space matching "master_id"; useful when the corresponding thread is
// being migrated elsewhere.
void pfsg_stop_thread_pf(PFStreamGroup *sg, int master_id);


// "Producer" interface, from the memory subsystem

// From the memory subsystem: report that a prefetch generated by one of the
// streams has been satisfied.  "eff_access_type" is a CacheAccessType enum of
// the "strongest" access_type which the fill can satisfy; it may be stronger
// than the one generated by the prefetch, if it was promoted by the memory
// subsystem.  "filled_to_cache" is a flag indicating that the given block was
// also filled to the corresponding data cache, e.g. the cache miss occurred
// while this block was being prefetched, so the streambuf can remove its own
// copy.
void pfsg_pf_fill(PFStreamGroup *sg, LongAddr base_addr,
                  int eff_access_type, i64 ready_time,
                  int filled_to_cache);

// Note that an outstanding prefetch for the given block is having an
// additional memory request merged with it.  This is a somewhat magical
// signal that is delivered for free from potentially off-chip, so it
// shouldn't be used for ANY data management; it's just here for statistics
// collection.
//
// pf_came_first: flag, if true, the prefetch request came before the memory
// request being merged (i.e. the prefetch MAY have "won").  If false, the
// prefetch request came later, and is being merged with an outstanding memory
// request (i.e. prefetch lost or tied).  When true, this only implies a win
// if this is the _first_ merge involving this instance of an outstanding
// prefetch.  Later D-misses to the same block as a losing prefetch request
// will also come in with pf_came_first == 1, and it's up to the PFStreamGroup
// to tell the difference.
void pfsg_pf_merged(PFStreamGroup *sg, LongAddr base_addr, int pf_came_first);


// Reporting/debug routines
void pfsg_print_stats(const PFStreamGroup *sg, void *c_FILE_out,
                      const char *prefix);
void pfsg_dump(const PFStreamGroup *sg, void *c_FILE_out, const char *prefix);


// export/manipulate thread-relevant prefetcher state
PFStreamExported *pfsg_export(const PFStreamGroup *sg, int master_id);
// prefer_imported_streams, flag: imported streams always take precedence over
// existing streams
// imports_win_ties, flag: when comparing stream priority, imports win ties
void pfsg_import(PFStreamGroup *sg, const PFStreamExported *pf_exp,
                 int prefer_imported_streams, int imports_win_ties);

PFStreamExported *pfse_copy(const PFStreamExported *pf_exp);
void pfse_destroy(PFStreamExported *pf_exp);
void pfse_dump(const PFStreamExported *pf_exp, void *c_FILE_out,
               const char *prefix);
int pfse_empty(const PFStreamExported *pf_exp);
long pfse_estimate_size_bits(const PFStreamExported *pf_exp);


#ifdef __cplusplus
}
#endif

#endif  // PREFETCH_STREAMBUF_H