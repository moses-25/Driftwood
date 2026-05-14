const CheckoutProgress = ({ steps, currentStep }) => {
  return (
    <div className="flex items-center justify-center mb-2">
      <ol className="flex items-center w-full max-w-lg">
        {steps.map((step, index) => {
          const isCompleted = index < currentStep
          const isActive = index === currentStep
          const isLast = index === steps.length - 1

          return (
            <li key={step} className={`flex items-center ${isLast ? '' : 'flex-1'}`}>
              <div className="flex flex-col items-center gap-1.5">
                <div className={`flex h-9 w-9 items-center justify-center rounded-full border-2 text-sm font-bold transition-all duration-300 ${
                  isCompleted ? 'border-caramel bg-caramel text-white'
                  : isActive ? 'border-white bg-white/10 text-white'
                  : 'border-white/20 bg-transparent text-white/30'
                }`}>
                  {isCompleted ? (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span className="font-tinos">{index + 1}</span>
                  )}
                </div>
                <span className={`text-xs font-medium whitespace-nowrap transition-colors duration-300 font-tinos ${
                  isActive ? 'text-white' : isCompleted ? 'text-caramel' : 'text-white/30'
                }`}>
                  {step}
                </span>
              </div>
              {!isLast && (
                <div className="flex-1 mx-2 mb-5">
                  <div className="h-px w-full bg-white/10 overflow-hidden">
                    <div className="h-full bg-caramel transition-all duration-500" style={{ width: isCompleted ? '100%' : '0%' }} />
                  </div>
                </div>
              )}
            </li>
          )
        })}
      </ol>
    </div>
  )
}

export default CheckoutProgress
