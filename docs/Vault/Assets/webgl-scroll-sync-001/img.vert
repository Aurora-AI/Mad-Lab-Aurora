// img.vert — DOM-to-NDC Coordinate Mapping
uniform vec2 u_resolution;   // canvas resolution
uniform vec2 u_scrollOffset;  // current scroll position
uniform vec2 u_domXY;         // DOM element top-left
uniform vec2 u_domWH;         // DOM element width/height

varying vec2 v_uv;

void main() {
    // 1. Calculate center position in pixel space
    vec2 pixelXY = u_domXY - u_scrollOffset + u_domWH * 0.5;

    // 2. Invert Y axis
    pixelXY.y = u_resolution.y - pixelXY.y;

    // 3. Scale plane to match DOM element size
    pixelXY += position.xy * u_domWH;

    // 4. Convert to NDC (-1 to 1)
    vec2 xy = pixelXY / u_resolution * 2. - 1.;

    v_uv = uv;
    gl_Position = vec4(xy, 0., 1.0);
}
