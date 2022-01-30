# UE4_Texture_compression

材质纹理压缩工具，理论上来说适合所有引擎，但开发时只针对UE4做了参考。

基于 PIL

首先要理解UE4 中纹理压缩模式，请参考：
UE4中的纹理压缩 —— Compression in UE4 - Helo的文章 - 知乎 https://zhuanlan.zhihu.com/p/401111461

通常做纹理压缩策略时都会考虑使用例如ps 或 substance 等软件，但是合并纹理的操作通常来说比较简单，一些简单的开发流程也着实没必要再引入其他工具，遂做此程序，望诸君能轻装上阵。

基础使用方式：

python texture_merge_tool.py [mode] [textures path]

textures path 可以是一个包含所有要处理的纹理的目录，也可以是包含多个文件夹的纹理集合，程序会逐个这些目录下的所有纹理。

程序可以处理的纹理包括 base color，normal，ao，cavity，diplacement，roughness 六种纹理，为了识别纹理种类请保证以上六种纹理分别以以下后缀结尾：
 "_albedo.jpg"，"_normal.jpg"，"_ao.jpg"，"_cavity.jpg"，"_displacement.jpg"，"_roughness.jpg"
 

mode 有两个选项：simple / high / mix

simple 模式会将 ao，displacement，roughness 三种纹理合并为一张jpg，分别占用 RGB 三个通道。
在ue 中使用时，base color 和 normal 直接只用相应纹理， ao，displacement，roughness 三个值从simple 模式合并后纹理中取用。
特点是使用简单，但是相比 high 多一次采样。

simple 模式运行后输出一张新纹理，名为ao_d_r.jpg


high 模式首先合并 base color 和 roughness 两种纹理，roughness 占用 alphe 通道，纹理保存为png。使用时注意调整ue 中的压缩模式以保证质量。
normal，ao，cavity，displacement 四纹理合并为一张纹理，normal 占用 RG 两通道。ao 和 cavity 使用正片叠底模式，即 a * b / 255。最后 displacement 占用alpha 通道。
此模式的特点是相对simple 而言少一次采样，但是效果较simple 差，使用也稍微麻烦一些。

high 模式运行后输出两张新纹理，分别为 a_r.png 和 n_ao_d.png

high 模式纹理在 ue 中使用方式如下图：
<img width="1120" alt="image" src="https://user-images.githubusercontent.com/38783813/151701597-0e74cdde-bcb4-4aac-9d35-af495b98b231.png">

图中 “inpout cr” 纹理为 ar.png，“input noh” 纹理为naob.png


mix 模式是在simple 的模式上，使用high 模式中对ao 的处理，对ao 的压缩和解压参考high。
mix 模式的效果最好。输出新纹理名为 ac_d_r.jpg

high 模式来自 youtube 一大神，此君shader 技能天下无双，又好为人师，希望诸君多多关注。
https://youtu.be/mEDoy-N1ODQ

