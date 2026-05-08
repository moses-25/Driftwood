import { useEffect, useRef } from 'react'

export default function Cursor() {
  const circleRef = useRef(null)

  useEffect(() => {
    const circle = circleRef.current
    if (!circle) return

    // Only show on pointer-capable devices
    if (!window.matchMedia('(pointer: fine)').matches) return

    circle.style.display = 'block'

    const onMouseMove = (e) => {
      circle.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`
    }

    const onPointerDown = () => {
      circle.style.scale = '0.25'
      setTimeout(() => { circle.style.scale = '1' }, 150)
    }

    window.addEventListener('mousemove', onMouseMove, { passive: true })
    document.addEventListener('pointerdown', onPointerDown)

    return () => {
      window.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('pointerdown', onPointerDown)
    }
  }, [])

  return (
    <div
      ref={circleRef}
      aria-hidden="true"
      className="fixed top-0 left-0 pointer-events-none z-[9999] hidden"
      style={{
        width: 32,
        height: 32,
        marginLeft: -16,
        marginTop: -16,
        borderRadius: '50%',
        border: '2px solid #c2620a',
        backgroundColor: 'rgba(194,98,10,0.2)',
        transition: 'scale 0.15s ease',
        willChange: 'transform',
      }}
    />
  )
}
