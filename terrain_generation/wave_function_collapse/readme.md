# Wave Function Collapse

## General

## Definitions

- **Bitmap**: Your input image, that serves as the source image from which $NxN$ patters are extracted. A bitmap is a type of memory organization or image file format used to stored digital images. It consists of a rectangular grid of pixels, where each pixel reperesents a color or shade. This description sound similar to a 'normal' image. However, originally a bitmap reffered to a binary image, where each pixel was either black or white (1-bit per pixel), in that sense it really is a map of bits. It is often used referring to uncompressed, or minimally processed data. In practice, bitmap often refers to any raster image, meaning an image made of pixels rather than vectors. It can also store multiple bits per pixel (8-bit grayscale, 24-bit color or 32-bit with alpha layer).

## Algorithm

## Model versions

## Resources

- The [original repository](https://github.com/mxgmn/WaveFunctionCollapse/tree/master) by [mxgmn](https://github.com/mxgmn). However, I don't think the algorithm description is formulated properly. I spend a lot of time trying to figure out what the adjacency rules precisely are for the constraint propagation, also for different versions of the algorithm. I think it could have been written more clearly. I also don't see the point of the quantum mechanics analogy. Introducing this makes it unnecessarily complex; for example, entropy is just a fancy word for the 'number of options' or 'number of possibilities' in the context of the wave function collapse algorithm. You can probably have a good discussion whether it is correct to use quantum mechanical terms in this context, but I think that's besides the point and also wrong. It is wrong because entropy in quantum mechanics or thermodynamics describes a different type of system; it is based on the physical arrangements of molecules on a microscopic level while still appearing the same on the macro level, while in the context of WFC it's just the number of options for a element in your variable that represents the grid. It is besides the point because code should be simple and easy to understand, and trying to explain the concepts related to your procedural generation algorithm (or however you want to describe it) in terms of quantum mechanical concepts, doesn't help with this. It does sound fancy though, and it grabs your attention, so I guess it's just good marketing.