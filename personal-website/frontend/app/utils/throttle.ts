export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  interval: number
): (...args: Parameters<T>) => void {
  let lastTime = 0

  return function (...args: Parameters<T>) {
    const now = Date.now()
    if (now - lastTime >= interval) {
      fn(...args)
      lastTime = now
    }
  }
}