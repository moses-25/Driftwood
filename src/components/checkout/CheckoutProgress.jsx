const CheckoutProgress = ({ steps, currentStep }) => {
  return (
    <div className="flex items-center justify-center">
      <ol className="flex items-center w-full max-w-lg">
        {steps.map((step, index) => {
          const isCompleted = index < currentStep
          const isActive = index === currentStep
          const isLast = index === steps.length - 1

          return (
            <li key={step} className={`flex items-center ${isLast ? '' : 'flex-1'}`}>
              {/* Step circle + label */}
              <div className="flex flex-col items-center gap-1.5">
                <div
                  className={`flex h-9 w-9 items-center justify-center rounded-full border-2 text-sm font-bold transition-all duration-300 ${
                    isCompleted
                      ? 'border-amber-500 bg-amber-500 text-slate-900'
                      : isActive
                      ? 'border-amber-400 bg-amber-400/15 text-amber-300 shadow-[0_0_16px_rgba(251,191,36,0.35)]'
                      : 'border-white/20 bg-white/5 text-slate-500'
                  }`}
                >
                  {isCompleted ? (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span>{index + 1}</span>
                  )}
                </div>
                <span
                  className={`text-xs font-medium whitespace-nowrap transition-colors duration-300 ${
                    isActive ? 'text-amber-300' : isCompleted ? 'text-amber-500' : 'text-slate-500'
                  }`}
                >
                  {step}
                </span>
              </div>

              {/* Connector line */}
              {!isLast && (
                <div className="flex-1 mx-2 mb-5">
                  <div className="h-0.5 w-full rounded-full bg-white/10 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-amber-500 to-orange-500 transition-all duration-500"
                      style={{ width: isCompleted ? '100%' : '0%' }}
                    />
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
