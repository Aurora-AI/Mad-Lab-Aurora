import { FallingPattern } from "./index";

export default function DefaultDemo() {
	return (
		<div className="w-full relative min-h-screen bg-black">
      {/* Aurora Interpretation: Low opacity primary falling elements */}
			<FallingPattern 
        color="rgba(59, 130, 246, 0.3)" 
        backgroundColor="transparent"
        className="h-screen [mask-image:radial-gradient(ellipse_at_center,transparent,black)]" 
      />
			<div className="absolute inset-0 z-10 flex flex-col items-center justify-center text-white">
				<h1 className="font-mono text-7xl font-extrabold tracking-tighter mix-blend-difference">
					FALLING PATTERN
				</h1>
        <p className="text-zinc-500 font-medium tracking-widest mt-4">KINETIC TEXTURE PROTOCOL</p>
			</div>
		</div>
	);
}
