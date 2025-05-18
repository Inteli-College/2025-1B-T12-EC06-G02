import Image from "next/image";

export default function BackgroundImage({ children }) {
  return (
    <div className="relative w-full min-h-screen overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 -z-10">
        <Image
          src="/cityscape-background.png"
          alt="City Background"
          fill
          quality={100}
          priority
          className="object-cover brightness-90"
        />
      </div>

      {/* Semi-transparent Overlay */}
      <div className="absolute inset-0 bg-white/60 backdrop-blur-sm" />

      {/* Content */}
      <div className="relative z-10 flex items-center justify-center h-full">
        {children}
      </div>
    </div>
  );
}
