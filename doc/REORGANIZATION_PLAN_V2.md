# Documentation Reorganization Plan V2
**Clear Structure with Leveled Documents**

**Date**: 2025-01-21
**Status**: Ready for Execution
**Goal**: Professional, leveled documentation structure with clear naming

---

## 🎯 New Structure Overview

### Leveled Documentation System

```
doc/
├── INDEX.md (Master navigation - replaces 00_START_HERE)
│
├── architecture/
│   ├── architecture-level-1-overview.md (High-level system design)
│   ├── architecture-level-2-components.md (Detailed components)
│   ├── architecture-level-3-implementation.md (Implementation details)
│   └── context-understanding.md (Specialized architecture)
│
├── roadmap/
│   ├── roadmap-level-1-vision.md (Strategic vision & milestones)
│   ├── roadmap-level-2-phases.md (Development phases)
│   ├── roadmap-level-3-sprints.md (Detailed sprint plans)
│   └── roadmap-status.md (Current progress tracking)
│
├── protocols/
│   ├── protocols-level-1-foundation.md (Core protocols)
│   ├── protocols-level-2-neurogenesis.md (Dynamic agent protocols)
│   ├── protocols-level-3-advanced.md (Advanced features)
│   └── protocols-migration.md (Migration strategies)
│
├── implementation/
│   ├── sprint-1-2-foundation.md (Critical foundation)
│   ├── sprint-3-performance.md (Async & performance)
│   ├── sprint-4-5-context.md (Context understanding)
│   ├── sprint-6-memory.md (Tiered memory)
│   ├── sprint-7-multimodal.md (Multi-modal learning)
│   ├── sprint-8-autonomous.md (Autonomous cognition)
│   └── implementation-status.md (What's complete)
│
├── guides/
│   ├── quick-start.md
│   ├── getting-started.md
│   ├── testing-guide.md
│   ├── monitoring-guide.md
│   └── contributing.md
│
├── technical/
│   ├── graph-schema.md
│   ├── schema-migration.md
│   ├── orchestrator-service.md
│   ├── multilanguage-support.md
│   └── production-infrastructure.md
│
└── archive/
    └── historical-evolution.md (Merged old files)
```

---

## 📊 Content Mapping & Merging Strategy

### Architecture Files (Leveled Approach)

**architecture-level-1-overview.md** (~800 lines)
- **Merge from:**
  - Current: ARCHITECTURE.md (lines 1-250 - philosophy, overview)
  - Old: design and concept.md (core concepts)
  - Old: 1.md (initial vision)
- **Content:**
  - Core philosophy & principles
  - High-level system overview
  - Component diagram
  - Process flow

**architecture-level-2-components.md** (~900 lines)
- **Merge from:**
  - Current: ARCHITECTURE.md (lines 251-476 - component details)
  - Old: SEGMENT_1_ARCHITECTURE_FINDINGS.md
- **Content:**
  - Detailed component descriptions
  - Agent types and capabilities
  - Services architecture
  - Integration patterns

**architecture-level-3-implementation.md** (~950 lines)
- **Merge from:**
  - Current: CONTEXT_UNDERSTANDING_ARCHITECTURE.md
  - Current: Enhancing Project Myriad Towards Human-Like Cognition.md
- **Content:**
  - Implementation specifics
  - Code-level architecture
  - Advanced features design
  - Evolution strategies

**context-understanding.md** (keep separate, ~600 lines)
- Specialized deep-dive on context architecture

---

### Roadmap Files (Leveled Approach)

**roadmap-level-1-vision.md** (~750 lines)
- **Merge from:**
  - Current: ROADMAP.md (lines 1-100 - vision & summary)
  - Old: roadmap.md (initial vision)
  - Old: roadmapPlus.md (expanded vision)
- **Content:**
  - Strategic vision
  - Major milestones
  - Revolutionary achievements
  - Future direction

**roadmap-level-2-phases.md** (~900 lines)
- **Merge from:**
  - Current: ROADMAP.md (lines 101-400 - phases overview)
  - Old: roadmapPlusPlus.md (phase details)
  - Old: roadmapFinal.md (finalized phases)
- **Content:**
  - Foundation phases (1-5)
  - Enhancement phases (6-8)
  - Advanced phases (9-12)
  - Phase dependencies

**roadmap-level-3-sprints.md** (~950 lines)
- **Merge from:**
  - Current: ROADMAP.md (lines 401-593 - detailed plans)
  - Current: COMPREHENSIVE_IMPLEMENTATION_PLAN.md (sprint details)
- **Content:**
  - Detailed sprint breakdowns
  - Task lists
  - Success criteria
  - Timeline estimates

**roadmap-status.md** (~400 lines)
- **Merge from:**
  - Current: STATUS.md
  - Old: SYSTEM_STATUS_REPORT.md
- **Content:**
  - Current implementation status
  - Metrics and performance
  - Production readiness
  - Next priorities

---

### Protocols Files (Leveled Approach)

**protocols-level-1-foundation.md** (~950 lines)
- **Merge from:**
  - Current: PROTOCOLS.md (lines 1-750)
  - Old: PROTOCOLS.md (foundation concepts)
- **Content:**
  - Architecture overview
  - Foundation protocols (Phase 1)
  - Graph database protocols
  - Basic communication

**protocols-level-2-neurogenesis.md** (~900 lines)
- **Merge from:**
  - Current: PROTOCOLS.md (lines 751-1500)
  - Old: PROTOCOLSPlus.md (neurogenesis additions)
- **Content:**
  - Neurogenesis protocols (Phase 2N)
  - Network protocols (Phase 2)
  - Evolution protocols (Phase 3)
  - Hebbian learning

**protocols-level-3-advanced.md** (~950 lines)
- **Merge from:**
  - Current: PROTOCOLS.md (lines 1501-2276)
  - Old: PROTOCOLSPlusPlus.md (advanced features)
  - Old: PROTOCOLSFinal.md (finalized protocols)
- **Content:**
  - Advanced features (Phase 4)
  - Genesis & multi-modal (Phase 5)
  - Advanced learning (Phase 6)
  - Autonomous cognition (Phase 7)

**protocols-migration.md** (~400 lines)
- **Content:**
  - Implementation guidelines
  - Migration strategies
  - Version compatibility
  - Best practices

---

### Implementation Files (Sprint-Based)

**sprint-1-2-foundation.md** (~850 lines)
- **From:** COMPREHENSIVE_IMPLEMENTATION_PLAN.md (Sprint 1-2 section)
- **Content:**
  - Orchestrator microservice extraction
  - Resource limits for neurogenesis
  - Graph schema enforcement
  - Production monitoring stack

**sprint-3-performance.md** (~600 lines)
- **From:** COMPREHENSIVE_IMPLEMENTATION_PLAN.md (Sprint 3 section)
- **Content:**
  - Async orchestrator conversion
  - Circuit breakers
  - Performance optimization

**sprint-4-5-context.md** (~900 lines)
- **From:** COMPREHENSIVE_IMPLEMENTATION_PLAN.md (Sprint 4-5 section)
- **Content:**
  - Conversation session manager
  - Reference resolution
  - Context understanding

**sprint-6-memory.md** (~700 lines)
- **From:** COMPREHENSIVE_IMPLEMENTATION_PLAN.md (Sprint 6 section)
- **Content:**
  - Tiered memory architecture
  - STM/MTM/LTM implementation

**sprint-7-multimodal.md** (~600 lines)
- **From:** COMPREHENSIVE_IMPLEMENTATION_PLAN.md (Sprint 7 section)
- **Content:**
  - Multi-modal foundation
  - Image/audio embeddings
  - Learning pipeline

**sprint-8-autonomous.md** (~800 lines)
- **From:** COMPREHENSIVE_IMPLEMENTATION_PLAN.md (Sprint 8 section)
- **Content:**
  - Self-awareness
  - Curiosity engine
  - Autonomous loop

**implementation-status.md** (~500 lines)
- **Merge from:**
  - Current: IMPLEMENTATION_COMPLETE.md
  - Current: MISSING_COMPONENTS_ANALYSIS.md
  - Current: MULTILANGUAGE_IMPLEMENTATION_STATUS.md
- **Content:**
  - Completed features
  - Missing components
  - Implementation metrics
  - Quality status

---

### Guides (User-Facing)

**quick-start.md** (keep as-is)
- From: QUICK_START.md

**getting-started.md** (keep as-is)
- From: GETTING_STARTED.md

**testing-guide.md** (keep as-is)
- From: TESTING_GUIDE.md

**monitoring-guide.md** (keep as-is)
- From: MONITORING_GUIDE.md

**contributing.md** (move from root)
- From: ../CONTRIBUTING.md

---

### Technical Documentation

**graph-schema.md** (keep as-is)
- From: GRAPH_SCHEMA.md

**schema-migration.md** (keep as-is)
- From: SCHEMA_MIGRATION_GUIDE.md

**orchestrator-service.md** (keep as-is)
- From: ORCHESTRATOR_MICROSERVICE_IMPLEMENTATION.md

**production-infrastructure.md** (keep as-is)
- From: PRODUCTION_INFRASTRUCTURE_IMPLEMENTATION.md

---

### Archive

**historical-evolution.md** (~800 lines)
- **Merge from all Old/ files:**
  - Old/1.md
  - Old/design and concept.md
  - Enhancing Project Myriad Towards Human-Like Cognition.md
  - New way.md
- **Content:**
  - Historical design evolution
  - Deprecated approaches
  - Lessons learned
  - Evolution timeline

---

## 🔧 Execution Plan

### Step 1: Create Directory Structure
```bash
mkdir -p doc/architecture
mkdir -p doc/roadmap
mkdir -p doc/protocols
mkdir -p doc/implementation
mkdir -p doc/guides
mkdir -p doc/technical
mkdir -p doc/archive
```

### Step 2: Build Leveled Architecture Files
1. Create `architecture-level-1-overview.md`
   - Merge: ARCHITECTURE.md (intro) + Old/design and concept.md + Old/1.md
   - Max 800 lines
   
2. Create `architecture-level-2-components.md`
   - Merge: ARCHITECTURE.md (components) + SEGMENT_1_ARCHITECTURE_FINDINGS.md
   - Max 900 lines
   
3. Create `architecture-level-3-implementation.md`
   - Merge: CONTEXT_UNDERSTANDING_ARCHITECTURE.md + Enhancing Project Myriad...
   - Max 950 lines

### Step 3: Build Leveled Roadmap Files
1. Create `roadmap-level-1-vision.md`
   - Merge: ROADMAP.md (vision) + Old/roadmap*.md (vision parts)
   - Max 750 lines
   
2. Create `roadmap-level-2-phases.md`
   - Merge: ROADMAP.md (phases) + Old/roadmap*.md (phase parts)
   - Max 900 lines
   
3. Create `roadmap-level-3-sprints.md`
   - From: ROADMAP.md (details) + COMPREHENSIVE_IMPLEMENTATION_PLAN.md (sprints)
   - Max 950 lines
   
4. Create `roadmap-status.md`
   - Merge: STATUS.md + Old/SYSTEM_STATUS_REPORT.md
   - Max 400 lines

### Step 4: Build Leveled Protocols Files
1. Create `protocols-level-1-foundation.md`
   - Split from: PROTOCOLS.md (lines 1-750) + Old/PROTOCOLS.md
   - Max 950 lines
   
2. Create `protocols-level-2-neurogenesis.md`
   - Split from: PROTOCOLS.md (lines 751-1500) + Old/PROTOCOLSPlus.md
   - Max 900 lines
   
3. Create `protocols-level-3-advanced.md`
   - Split from: PROTOCOLS.md (lines 1501-end) + Old/PROTOCOLSPlusPlus.md + PROTOCOLSFinal.md
   - Max 950 lines

### Step 5: Build Sprint Implementation Files
1. Create sprint-1-2-foundation.md (~850 lines)
2. Create sprint-3-performance.md (~600 lines)
3. Create sprint-4-5-context.md (~900 lines)
4. Create sprint-6-memory.md (~700 lines)
5. Create sprint-7-multimodal.md (~600 lines)
6. Create sprint-8-autonomous.md (~800 lines)
7. Create implementation-status.md (~500 lines)

### Step 6: Organize Guides & Technical Docs
1. Move/rename guides to doc/guides/
2. Move technical docs to doc/technical/
3. Update all file references

### Step 7: Create Archive
1. Create `historical-evolution.md` merging all Old/ content
2. Keep Old/ directory as-is for reference

### Step 8: Create Master Index
1. Create `INDEX.md` with:
   - Quick navigation
   - Reading paths (beginner → advanced)
   - File descriptions
   - Cross-references

---

## 📋 Navigation Structure

Each file will have:

**Header:**
```markdown
# Document Title

📚 **Level X of Y** | [Overview](../INDEX.md) | [Prev Level](link) | [Next Level](link)

**Related Documents:**
- [Related Doc 1](link)
- [Related Doc 2](link)

---
```

**Footer:**
```markdown
---

## Navigation

- **Next Level:** [Level X+1](link) - Go deeper
- **Previous Level:** [Level X-1](link) - Go higher  
- **Related:** [Related Topic](link)
- **Index:** [Documentation Home](../INDEX.md)
```

---

## ✅ Success Criteria

1. ✅ No file exceeds 1000 lines
2. ✅ Clear, professional naming (no long acronyms)
3. ✅ Leveled structure (level-1, level-2, level-3)
4. ✅ All Old/ content merged (not deleted)
5. ✅ Logical grouping by category
6. ✅ Easy navigation between levels
7. ✅ All original content preserved
8. ✅ Professional documentation structure

---

## 🎯 Benefits of New Structure

1. **Clear Progression:** Level 1 → 2 → 3 shows increasing detail
2. **Better Names:** `architecture-level-1-overview.md` vs `ARCHITECTURE.md`
3. **Topic Grouping:** architecture/, roadmap/, protocols/ directories
4. **Preserved History:** Old content merged, not discarded
5. **Professional:** Suitable for external documentation
6. **Maintainable:** Easy to update individual sections
7. **Discoverable:** Intuitive structure for new users

---

**Ready to Execute?** This plan creates a professional, leveled documentation system with clear names and proper merging of all historical content.