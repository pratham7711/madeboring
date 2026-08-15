import json, pathlib

BASE = ('MB monogram logo mark, {t}, deep forest green and bright mint on warm cream '
        'background, minimal geometric brand mark, letters M and B only, centred, '
        'square composition, no extra text, high contrast, professional')

T = [
 'letterpress deboss into thick cotton paper',
 'extruded isometric 3d blocks with flat shadow',
 'brushed metal plate with engraved letters',
 'stacked paper cut layers with soft drop shadow',
 'risograph print with slight ink misregistration',
 'blueprint technical drawing, thin white lines on deep green',
 'rubber stamp impression with ink bleed and broken edges',
 'neon tube sign with soft glow on dark ground',
 'transparent glass with refraction and caustics',
 'embroidered patch with dense stitched border',
 'cast concrete relief with subtle surface grain',
 'wood inlay marquetry, two tones of veneer',
 'hard enamel pin with polished metal outline',
 'terrazzo texture filling the letterforms',
 'glazed ceramic tile with slight glaze pooling',
 'folded origami paper forming the letters',
 'wax seal impression pressed into paper',
 'woven textile, visible warp and weft',
 'sandblasted frosted glass panel',
 'anodized aluminium with fine radial brushing',
 'injection moulded plastic with soft bevels',
 'printed circuit board copper traces',
 'topographic contour lines forming the letters',
 'halftone dot gradient across the mark',
 'flat design with a long diagonal shadow',
 'soft gradient mesh, smooth colour transition',
 'duotone screenprint with visible ink texture',
 'liquid chrome metal, mirror finish',
 'deep debossed leather with visible grain',
 'carved marble with fine veining',
 'chunky 8-bit pixel blocks',
 'thin wireframe mesh, isometric perspective',
 'dot matrix printer output, coarse dots',
 'bauhaus primitives, circle square triangle construction',
 'swiss international style, strict grid, tight tracking',
 'brutalist concrete slab, heavy and blunt',
 'art deco inlay with fine linear rays',
 'single continuous line drawing, one unbroken stroke',
 'thick rounded soft shapes, generous radii',
 'sharp angular crystalline facets',
 'overlapping transparent shapes with multiply blending',
 'negative space letters knocked out of a solid circle',
 'layered depth, letters at different z heights',
 'a single ribbon folded to form both letters',
 'modular square grid units assembling the letters',
 'stipple shading, fine dotted rendering',
 'isometric extrusion with a hard cast shadow',
 'liquid ink blot with organic bleeding edges',
 'laser etched into a dark anodised surface',
 'soft touch silicone with a tactile matte finish',
]

assert len(T) == 50, len(T)
prompts = [BASE.format(t=t) for t in T]

pathlib.Path('prompts.txt').write_text(
    '\n\n'.join('%02d. %s' % (i, p) for i, p in enumerate(prompts, 1)))
pathlib.Path('prompts.json').write_text(json.dumps(prompts, indent=1))
print('50 prompts written')
for i, p in enumerate(prompts[:2], 1):
    print(i, p[:110])
