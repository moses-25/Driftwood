import { useState, useEffect } from 'react';

/**
 * Optimized Google Maps Embed Component
 * Features:
 * - Lazy loading for better performance
 * - Error handling with fallback
 * - Loading state
 * - Retry mechanism
 * - Responsive design
 */
const MapEmbed = ({ 
  latitude = -1.2921, 
  longitude = 36.8219,
  zoom = 15,
  className = "",
  height = "h-72 md:h-96"
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [cacheKey] = useState(() => Date.now());

  // Generate Google Maps embed URL
  const mapUrl = `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.8!2d${longitude}!3d${latitude}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f${zoom}!3m3!1m2!1s0x0%3A0x0!2zMcKwMTcnMzEuMiJTIDM2wrA0OScxOC44IkU!5e0!3m2!1sen!2ske!4v${cacheKey}!5m2!1sen!2ske`;

  // Alternative: Direct Google Maps link for fallback
  const directMapUrl = `https://www.google.com/maps?q=${latitude},${longitude}&z=${zoom}`;

  useEffect(() => {
    // Reset error state when retrying
    if (retryCount > 0) {
      setHasError(false);
    }
  }, [retryCount]);

  const handleLoad = () => {
    setIsLoaded(true);
    setHasError(false);
  };

  const handleError = () => {
    console.warn('Map iframe failed to load');
    setHasError(true);
    setIsLoaded(true);
  };

  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
    setHasError(false);
    setIsLoaded(false);
  };

  return (
    <div className={`w-full ${height} relative overflow-hidden bg-slate-100 ${className}`}>
      
      {/* Loading State */}
      {!isLoaded && !hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-100 z-20">
          <div className="text-center text-slate-400">
            <svg 
              className="w-12 h-12 mx-auto mb-3 opacity-30 animate-pulse" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" 
              />
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" 
              />
            </svg>
            <p className="text-sm font-medium">Loading map...</p>
          </div>
        </div>
      )}

      {/* Error State with Fallback */}
      {hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-100 z-20">
          <div className="text-center px-6 max-w-md">
            <svg 
              className="w-12 h-12 mx-auto mb-3 text-slate-300" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" 
              />
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" 
              />
            </svg>
            <p className="text-sm font-medium text-slate-600 mb-1">
              Driftwood Café
            </p>
            <p className="text-xs text-slate-400 mb-4">
              Nairobi, Kenya
            </p>
            <div className="flex gap-2 justify-center">
              <button
                onClick={handleRetry}
                className="px-4 py-2 bg-espresso text-white text-xs font-semibold rounded-lg hover:bg-caramel transition-colors"
              >
                Retry Map
              </button>
              <a
                href={directMapUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg hover:bg-slate-300 transition-colors"
              >
                Open in Google Maps
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Google Maps Iframe */}
      {!hasError && (
        <iframe
          key={retryCount} // Force re-render on retry
          title="Driftwood Café location"
          src={mapUrl}
          width="100%" 
          height="100%"
          style={{ border: 0 }}
          allowFullScreen="" 
          loading="lazy" 
          referrerPolicy="no-referrer-when-downgrade"
          className="relative z-10"
          onLoad={handleLoad}
          onError={handleError}
        />
      )}

      {/* Direct Link Overlay (always available) */}
      <a
        href={directMapUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="absolute bottom-4 right-4 z-30 px-3 py-2 bg-white/95 backdrop-blur-sm text-espresso text-xs font-semibold rounded-lg shadow-md hover:bg-caramel hover:text-white transition-all duration-200 flex items-center gap-1.5"
      >
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
        Open in Maps
      </a>
    </div>
  );
};

export default MapEmbed;
