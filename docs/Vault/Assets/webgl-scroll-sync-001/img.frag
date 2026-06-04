// img.frag — Scroll-Driven Glitch & Motion Blur
precision highp float;

uniform sampler2D u_texture;
uniform float u_strength;
uniform float u_id;
uniform vec3 u_rands;

varying vec2 v_uv;

#define NUM_SAMPLES 5

// Hash functions for noise
float hash13(vec3 p3) {
    p3  = fract(p3 * .1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

vec4 hash43(vec3 p) {
	vec4 p4 = fract(vec4(p.xyzx)  * vec4(.1031, .1030, .0973, .1099));
    p4 += dot(p4, p4.wzxy+33.33);
    return fract((p4.xxyz+p4.yzzw)*p4.zywx);
}

void main() {
    vec3 color = vec4(0.0).rgb;
    vec2 uv = v_uv;

    // Stochastic horizontal offset (Glitch logic)
    vec4 rands = hash43(vec3(floor(sin(v_uv.x * 2. + u_rands.x * 6.283) * mix(3., 40., u_rands.y)) * 30., u_id, u_rands.z));
    
    // Activate offset on ~30% of horizontal lines
    vec2 uvOffset = vec2(0., (rands.x - .5) * 0.5 * (rands.y > .7 ? 1. : 0.)) / float(NUM_SAMPLES) * (0.05 + u_strength * 0.3);

    // Motion blur loop
    for (int i = 0; i < NUM_SAMPLES; i++) {
        color += texture2D(u_texture, uv).rgb;
        uv += uvOffset;
    }
    color /= float(NUM_SAMPLES);

    // Brighten with scroll intensity
    gl_FragColor = vec4(color * (1. + u_strength * 2.0), 1.0);
}
