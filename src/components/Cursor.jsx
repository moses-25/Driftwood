import { useEffect, useRef } from 'react'

export default function Cursor() {
  const circleRef = useRef(null)

  useEffect(() => {
    const circle = circleRef.current

    const onMouseMove = (e) => {
      circle.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`
    }

    const onPointerDown = () => {
      circle.style.scale = '0.25'
      setTimeout(() => { circle.style.scale = '1' }, 150)
    }

    window.addEventListener('mousemove', onMouseMove)
    document.addEventListener('pointerdown', onPointerDown)

    return () => {
      window.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('pointerdown', onPointerDown)
    }
  }, [])

  return (
    <div
      ref={circleRef}
      className="fixed top-0 left-0 pointer-events-none z-[9999]"
      style={{
        width: 32,
        height: 32,
        marginLeft: -16,
        marginTop: -16,
        borderRadius: '50%',
        border: '3px solid #c2620a',
        backgroundColor: 'rgba(194,98,10,0.35)',
        transition: 'scale 0.15s ease',
        willChange: 'transform',
      }}
    />
  )
}
