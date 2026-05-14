import { motion } from 'framer-motion'
import { containerVariants } from './animationVariants'

export default function StaggerContainer({
  children,
  className = '',
  variants = containerVariants,
  threshold = 0.1,
  once = true,
}) {
  return (
    <motion.div
      variants={variants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once, amount: threshold }}
      className={className}
    >
      {children}
    </motion.div>
  )
}
