export const TOTAL_MS = 60_000

/** The clock owns sequence rules; Vue owns scheduling and display. */
export class BreathingClock {
  constructor(now = () => performance.now()) {
    this.now = now
    this.state = 'idle'
    this.accumulated = 0
    this.segmentStart = 0
    this.started = 0
  }

  start() {
    this.started = this.segmentStart = this.now()
    this.accumulated = 0
    this.state = 'running'
    return this.snapshot()
  }

  snapshot() {
    const elapsed = this.state === 'running'
      ? this.accumulated + Math.max(0, this.now() - this.segmentStart)
      : this.accumulated
    const activeMs = Math.min(TOTAL_MS, elapsed)
    if (this.state === 'running' && activeMs >= TOTAL_MS) {
      this.accumulated = TOTAL_MS
      this.state = 'completed'
    }
    const inCycle = activeMs % 10_000
    const inhale = inCycle < 4_000
    const phaseMs = inhale ? inCycle : inCycle - 4_000
    const phaseDuration = inhale ? 4_000 : 6_000
    return {
      state: this.state,
      activeMs,
      cycle: Math.min(6, Math.floor(activeMs / 10_000) + 1),
      cyclesCompleted: Math.floor(activeMs / 10_000),
      phase: inhale ? 'Breathe in' : 'Breathe out',
      count: Math.ceil((phaseDuration - phaseMs) / 1_000),
      expansion: inhale ? phaseMs / phaseDuration : 1 - phaseMs / phaseDuration,
    }
  }

  pause() {
    const snapshot = this.snapshot()
    if (this.state === 'running') {
      this.accumulated = snapshot.activeMs
      this.state = 'paused'
    }
    return this.snapshot()
  }

  resume() {
    if (this.state === 'paused') {
      this.segmentStart = this.now()
      this.state = 'running'
    }
    return this.snapshot()
  }

  stop() {
    const snapshot = this.snapshot()
    if (this.state === 'running' || this.state === 'paused') {
      this.accumulated = snapshot.activeMs
      this.state = 'stopped'
    }
    return this.snapshot()
  }

  /** Wall timestamps are anchored to start and advanced by monotonic elapsed time. */
  outcome(startedAt, displayMode) {
    const snapshot = this.snapshot()
    if (!['stopped', 'completed'].includes(snapshot.state)) {
      throw new Error('Only a stopped or completed exercise can be saved.')
    }
    return {
      started_at: new Date(startedAt).toISOString(),
      ended_at: new Date(startedAt + Math.ceil(this.now() - this.started)).toISOString(),
      status: snapshot.state,
      active_duration_seconds: Math.floor(snapshot.activeMs) / 1_000,
      cycles_completed: snapshot.cyclesCompleted,
      display_mode: displayMode,
    }
  }
}
