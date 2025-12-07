const FloatingElements = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {/* Gradient orbs */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/15 rounded-full blur-3xl animate-float" style={{ animationDelay: '-3s' }} />
      <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-neon-pink/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '-5s' }} />
      
      {/* Floating education icons */}
      <div className="absolute top-[15%] right-[20%] opacity-20 animate-float" style={{ animationDelay: '-2s' }}>
        <svg className="w-12 h-12 text-primary" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 3L1 9l11 6 9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82Z"/>
        </svg>
      </div>
      
      <div className="absolute bottom-[25%] left-[15%] opacity-15 animate-float" style={{ animationDelay: '-4s' }}>
        <svg className="w-16 h-16 text-accent" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2Zm-5 14H7v-2h7v2Zm3-4H7v-2h10v2Zm0-4H7V7h10v2Z"/>
        </svg>
      </div>
      
      <div className="absolute top-[40%] right-[10%] opacity-10 animate-float" style={{ animationDelay: '-1s' }}>
        <svg className="w-20 h-20 text-neon-purple" viewBox="0 0 24 24" fill="currentColor">
          <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
        </svg>
      </div>
      
      <div className="absolute bottom-[40%] right-[30%] opacity-15 animate-float" style={{ animationDelay: '-6s' }}>
        <svg className="w-10 h-10 text-neon-green" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      </div>
      
      <div className="absolute top-[60%] left-[8%] opacity-20 animate-float" style={{ animationDelay: '-3.5s' }}>
        <svg className="w-14 h-14 text-neon-cyan" viewBox="0 0 24 24" fill="currentColor">
          <path d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.516 6.516 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5Z"/>
        </svg>
      </div>
      
      {/* Small dots */}
      <div className="absolute top-[20%] left-[40%] w-2 h-2 bg-primary rounded-full opacity-40 animate-bounce-slow" />
      <div className="absolute top-[70%] right-[25%] w-3 h-3 bg-accent rounded-full opacity-30 animate-bounce-slow" style={{ animationDelay: '-1s' }} />
      <div className="absolute bottom-[15%] left-[50%] w-2 h-2 bg-neon-pink rounded-full opacity-50 animate-bounce-slow" style={{ animationDelay: '-2s' }} />
      
      {/* Grid pattern overlay */}
      <div 
        className="absolute inset-0 opacity-[0.02]"
        style={{
          backgroundImage: `
            linear-gradient(hsl(var(--primary)) 1px, transparent 1px),
            linear-gradient(90deg, hsl(var(--primary)) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px'
        }}
      />
    </div>
  );
};

export default FloatingElements;
