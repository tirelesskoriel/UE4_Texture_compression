# UE4_Texture_compression

材质纹理压缩工具，理论上来说适合所有引擎，但开发时只针对UE4做了参考。

基于 PIL

首先要理解UE4 中纹理压缩模式，请参考：
UE4中的纹理压缩 —— Compression in UE4 - Helo的文章 - 知乎 https://zhuanlan.zhihu.com/p/401111461

基础使用方式：

python texture_merge_tool.py [mode] [textures path]

mode 有两个选项：simple / high

simple 模式会将 ao，displacement，roughness 三种纹理合并为一张jpg，分别占用 RGB 三个通道。
在ue 中使用时，base color 和 normal 贴图直接采样， ao，displacement，roughness 三个值从simple 模式合并后贴图中取用。
特点是使用简单，但是相比 high 多一次采样。


high 模式首先合并 base color 和 roughness 两种纹理，roughness 占用 alphe 通道，纹理保存为png。使用时注意调整ue 中的压缩模式以保证质量。
normal，ao，cavity，displacement 四纹理合并为一张纹理，normal 占用 RG 两通道。ao 和 cavity 使用正片叠底模式，即 a * b / 255。最后 displacement 占用alpha 通道。
此模式的特点是相对simple 而言少一次采样，但是效果较simple 差，使用也稍微麻烦一些。

high 模式纹理在 ue 中使用方式如下图：
<img width="1120" alt="image" src="https://user-images.githubusercontent.com/38783813/151701597-0e74cdde-bcb4-4aac-9d35-af495b98b231.png">

