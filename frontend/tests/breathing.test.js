import test from 'node:test'
import assert from 'node:assert/strict'
import { BreathingClock } from '../src/breathing.js'

function fixture() {
  let now = 0
  const clock = new BreathingClock(() => now)
  return { clock, advance: (ms) => { now += ms } }
}

test('six fixed cycles use four-second inhales and six-second exhales', () => {
  const { clock, advance } = fixture()
  clock.start()
  for (let cycle = 1; cycle <= 6; cycle++) {
    assert.equal(clock.snapshot().cycle, cycle)
    assert.equal(clock.snapshot().phase, 'Breathe in')
    assert.equal(clock.snapshot().count, 4)
    advance(4_000)
    assert.equal(clock.snapshot().phase, 'Breathe out')
    assert.equal(clock.snapshot().count, 6)
    advance(6_000)
  }
  assert.equal(clock.snapshot().state, 'completed')
  assert.equal(clock.snapshot().cyclesCompleted, 6)
  assert.equal(clock.snapshot().activeMs, 60_000)
})

test('pause freezes phase/count and excludes voluntary time', () => {
  const { clock, advance } = fixture()
  clock.start()
  advance(5_500)
  const paused = clock.pause()
  advance(80_000)
  assert.deepEqual(clock.snapshot(), paused)
  clock.resume()
  advance(500)
  assert.equal(clock.snapshot().activeMs, 6_000)
  assert.equal(clock.snapshot().count, 4)
})

test('Stop freezes an early exit and ignores later ticks/resume', () => {
  const { clock, advance } = fixture()
  clock.start()
  advance(20_250)
  const stopped = clock.stop()
  advance(100_000)
  assert.deepEqual(clock.resume(), stopped)
  assert.deepEqual(clock.snapshot(), stopped)
  assert.equal(stopped.cyclesCompleted, 2)
  assert.equal(stopped.state, 'stopped')
})

test('delayed completion callback caps active time at sixty seconds', () => {
  const { clock, advance } = fixture()
  clock.start()
  advance(60_040)
  assert.equal(clock.snapshot().state, 'completed')
  const result = clock.outcome(Date.parse('2026-10-20T12:00:00Z'), 'text')
  assert.equal(result.active_duration_seconds, 60)
  assert.equal(result.ended_at, '2026-10-20T12:01:00.040Z')
})

test('a new start resets earlier time and pause state', () => {
  const { clock, advance } = fixture()
  clock.start()
  advance(30_000)
  clock.pause()
  advance(100_000)
  assert.equal(clock.start().activeMs, 0)
  assert.equal(clock.snapshot().cycle, 1)
  assert.equal(clock.snapshot().count, 4)
})

test('terminal payload preserves pause time in timestamps, not active duration', () => {
  const { clock, advance } = fixture()
  const started = Date.parse('2026-10-20T12:00:00Z')
  clock.start()
  advance(20_000)
  clock.pause()
  advance(5_000)
  clock.stop()
  assert.deepEqual(clock.outcome(started, 'text'), {
    started_at: '2026-10-20T12:00:00.000Z',
    ended_at: '2026-10-20T12:00:25.000Z',
    status: 'stopped',
    active_duration_seconds: 20,
    cycles_completed: 2,
    display_mode: 'text',
  })
})

test('no active session can be saved as a terminal outcome', () => {
  const { clock } = fixture()
  clock.start()
  assert.throws(() => clock.outcome(Date.now(), 'text'), /Only a stopped/)
})
