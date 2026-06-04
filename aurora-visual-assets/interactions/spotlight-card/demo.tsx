import { GlowCard } from "./index";

export function Default(){
  return(
    <div className="w-screen h-screen flex flex-row items-center justify-center gap-10 custom-cursor">
      <GlowCard>
        <div className="flex flex-col gap-2">
          <h3 className="text-xl font-bold text-white">Aurora Spotlight</h3>
          <p className="text-sm text-zinc-400">Fixed viewport coordinate syncing across components.</p>
        </div>
      </GlowCard>
      <GlowCard glowColor="purple">
        <div className="flex flex-col gap-2">
          <h3 className="text-xl font-bold text-white">Deep Purple</h3>
          <p className="text-sm text-zinc-400">Advanced CSS mask compositing for sub-pixel edges.</p>
        </div>
      </GlowCard>
      <GlowCard glowColor="orange">
        <div className="flex flex-col gap-2">
          <h3 className="text-xl font-bold text-white">Editorial Glow</h3>
          <p className="text-sm text-zinc-400">DNA Dark Editorial: Precision, Silence, Weight.</p>
        </div>
      </GlowCard>
    </div>
  );
};
