import {
  ImageComparison,
  ImageComparisonImage,
  ImageComparisonSlider
} from "./index";

export default function ImageComparisonBasic() {
  const natureImg = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=1200";
  
  return (natureImgnatureImg
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
        <ImageComparison className="aspect-video w-full" enableHover>
          <ImageComparisonImage
            src={natureImg}
            className="grayscale brightness-50"
            alt="Before - Grayscale"
            position="left"
          />
          <ImageComparisonImage
            src={natureImg}
            alt="After - Full Color"
            position="right"
          />
          <ImageComparisonSlider className="w-0.5 bg-white/40 backdrop-blur-md">
            <div className="absolute top-1/2 left-1/2 size-8 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white/10 border border-white/20 backdrop-blur-lg flex items-center justify-center shadow-xl">
              <div className="size-1.5 rounded-full bg-white animate-pulse" />
            </div>
          </ImageComparisonSlider>
        </ImageComparison>
      </div>
    </div>
  );
}
