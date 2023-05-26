# RenderdocTools

## FrameParser

FrameParser用于分析从手机Renderdoc截帧rdc文件保存下来的txt文本

可以将各个绘制阶段（Pass）的相关数据进行统计并输出可读信息

rdc文件必须从手机截取，且通过vulkan渲染，分析过程与ue的管线设计是耦合的

目前可以分析的Pass包括：
- ShadowDepthPass
- MobileRenderPrePass
- MobileBasePass
- Translucency

统计的内容包括各pass中的draw command数量和triangle数量，最后会统计总和数量

统计信息会首先输出到控制台，然后输出一个csv文件，文件名与输入文件相同

使用命令为：py FrameParser.py Frame.txt