import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'

export default function FadeUp({
  children,
  delay = 0,
  duration = 0.7,
  className = '',
}) {
  const { ref, inView } = useInView({
    threshold: 0.15,
    triggerOnce: true,
  })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{
        duration,
        delay,
        ease: [0.25, 0.1, 0.25, 1],
      }}
      className={className}
    >
      {children}
    </motion.div>
  )
}