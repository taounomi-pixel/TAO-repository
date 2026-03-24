from manim import *

class GaokaoMath(Scene):
    def play(self, *args, **kwargs):
        # 沿用您的加速习惯，为 Write 和 ReplacementTransform 提供 1.2 倍速加速
        if any(isinstance(arg, (Write, ReplacementTransform)) for arg in args):
            if "run_time" in kwargs:
                kwargs["run_time"] /= 1.2
            else:
                kwargs["run_time"] = 1.0 / 1.2
        super().play(*args, **kwargs)

    def construct(self):
        # ==========================================
        # 全局配置：初始化支持中文的 LaTeX 模板
        # ==========================================
        ctex = TexTemplate()
        ctex.add_to_preamble(r"\usepackage[UTF8]{ctex}")

        # ==========================================
        # 第一段画面：情绪引入
        # ==========================================
        text1 = Tex(r"$2024$ 新高考一卷的这道题你还会做吗？", tex_template=ctex, color=RED_A)
        text1.scale(0.7)
        
        # 控制不透明度实现平滑的放大逐字写出效果
        # 注意：Tex 对象在取路径时通常储存在索引 [0] 中
        for char in text1[0]:
            char.set_opacity(0)
            
        time_tracker = ValueTracker(0)
        def reveal_chars(mob):
            progress = time_tracker.get_value()
            num_chars = len(mob[0])
            if num_chars == 0:
                return
            for i, char in enumerate(mob[0]):
                start_p = i / num_chars * 0.8
                char.set_opacity(min(max((progress - start_p) / 0.2, 0), 1))
                
        text1.add_updater(reveal_chars)
        
        self.play(
            text1.animate.scale(1/0.7),
            time_tracker.animate.set_value(1),
            run_time=2.5
        )
        text1.remove_updater(reveal_chars)
        self.wait(1)
        
        # 第一段文字淡出
        self.play(FadeOut(text1))

        # ==========================================
        # 第二段画面：引出原题和改编题
        # ==========================================
        # 第一部分原题文字，重新断句排版，左对齐，首行缩进
        text2 = VGroup(
            Tex(r"\qquad 甲乙两人各有四张卡片，每张卡片上标有一个数字，甲的卡片", tex_template=ctex, color=BLUE),
            Tex(r"上分别标有数字 $1, 3, 5, 7$，乙的卡片上分别标有数字 $2, 4, 6, 8$，", tex_template=ctex, color=BLUE),
            Tex(r"两人进行四轮比赛，在每轮比赛中，两人各自从自己持有的卡片", tex_template=ctex, color=BLUE),
            Tex(r"中随机选一张，并比较所选卡片上的数字大小，数字大的人得 $1$", tex_template=ctex, color=BLUE),
            Tex(r"分，数字小的人得 $0$ 分，然后各自弃置此轮所选的卡片(弃置的", tex_template=ctex, color=BLUE),
            Tex(r"卡片在此后的轮次中不能使用)，则四轮比赛后，甲的总得分不小", tex_template=ctex, color=BLUE),
            Tex(r"于 $2$ 的概率为多少？", tex_template=ctex, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.65).move_to(ORIGIN)
        
        self.play(Write(text2))
        self.wait(2.5)
        
        # 第二部分改编题目文字，重新断句排版，左对齐，首行缩进
        text3 = VGroup(
            Tex(r"\qquad 甲有分别标有 $1, 3, \dots, 2n-1$ 的 $n$ 张牌，乙有分别标有", tex_template=ctex, color=WHITE),
            Tex(r"$2, 4, \dots, 2n$ 的 $n$ 张牌，每局比赛甲、乙各出一张牌，数字大的", tex_template=ctex, color=WHITE),
            Tex(r"得 $1$ 分，小的得 $0$ 分，出过的牌则丢弃，设 $n$ 局后甲的得分", tex_template=ctex, color=WHITE),
            Tex(r"为 $X$，求 $X$ 的分布列", tex_template=ctex, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.75).move_to(ORIGIN)
        
        self.play(ReplacementTransform(text2, text3))
        self.wait(3)
        self.play(FadeOut(text3))

        # ==========================================
        # 第三段画面：引入递推关系与欧拉数
        # ==========================================
        s3_l1 = Tex(r"设甲得 $k$ 分的情况数为 $f(n,k)$", tex_template=ctex, color=WHITE)
        s3_l2 = Tex(r"通过分析最后一张牌的插入位置，分类讨论可得：", tex_template=ctex, color=LIGHT_GREY)
        s3_l3 = MathTex(r"f(n,k) = (k+1)f(n-1,k) + (n-k)f(n-1,k-1)", color=YELLOW)
        
        s3_group = VGroup(s3_l1, s3_l2, s3_l3).arrange(DOWN, buff=0.8).move_to(UP * 0.5)
        
        self.play(Write(s3_l1))
        self.wait(0.5)
        self.play(Write(s3_l2))
        self.wait(0.5)
        self.play(Write(s3_l3))
        self.wait(1.5)
        
        # 前两行淡出，递推式移到中央
        self.play(
            FadeOut(s3_l1),
            FadeOut(s3_l2),
            s3_l3.animate.move_to(ORIGIN)
        )
        self.wait(0.5)
        
        # 递推式下方出现“欧拉数”文字
        euler_text = Tex("欧拉数 (Eulerian Numbers)", tex_template=ctex, color=GOLD).next_to(s3_l3, DOWN, buff=1)
        self.play(Write(euler_text))
        self.wait(2)

        # ==========================================
        # 第四段画面：召唤母函数恒等式
        # ==========================================
        self.play(
            FadeOut(s3_l3),
            euler_text.animate.to_edge(UP)
        )
        self.wait(0.5)
        
        s4_l1 = MathTex(r"A_n(y) = \sum_{k=0}^{n} f(n,k) y^k", color=BLUE_A)
        s4_l2 = MathTex(
            r"\frac{A_n(y)}{(1-y)^{n+1}} = \sum_{j=0}^{\infty} (j+1)^n y^j",
            color=PURPLE_A
        )
        
        s4_group = VGroup(s4_l1, s4_l2).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        br_text = Tex("引入母函数恒等式", tex_template=ctex, color=YELLOW).scale(0.6).to_corner(DR)
        
        self.play(Write(s4_l1))
        self.wait(0.5)
        self.play(Write(s4_l2), Write(br_text))
        self.wait(2)

        # ==========================================
        # 第五段画面：移项与二项式展开
        # ==========================================
        # 保留第四段第二行等式，上移至中央（偏上作为新的第一行）
        self.play(
            FadeOut(euler_text),
            FadeOut(s4_l1), 
            FadeOut(br_text),
            s4_l2.animate.move_to(UP * 1)
        )
        self.wait(1)
        
        # 发生移项变换
        s5_eq1 = MathTex(
            r"A_n(y) = (1-y)^{n+1} \sum_{j=0}^{\infty} (j+1)^n y^j",
            color=BLUE
        ).move_to(s4_l2.get_center())
        s5_t1 = Tex("移项得", tex_template=ctex, color=YELLOW).scale(0.7).next_to(s5_eq1, DOWN, buff=1)
        
        # 使用 TransformMatchingShapes 基于 SVG 路径匹配形状飞跃，完美避开 LaTeX 编译边界问题
        self.play(TransformMatchingShapes(s4_l2, s5_eq1), Write(s5_t1))
        self.wait(1)
        
        # 二项式展开
        s5_eq2 = MathTex(
            r"A_n(y) = \left[ \sum_{m=0}^{n+1} \binom{n+1}{m} (-1)^m y^m \right] \cdot \left[ \sum_{j=0}^{\infty} (j+1)^n y^j \right]",
            color=PURPLE_A
        ).move_to(s5_eq1.get_center())
        s5_t2 = Tex("二项式展开", tex_template=ctex, color=PURPLE).scale(0.7).move_to(s5_t1.get_center())
        
        self.play(TransformMatchingShapes(s5_eq1, s5_eq2), ReplacementTransform(s5_t1, s5_t2))
        self.wait(2)

        # ==========================================
        # 第六段画面：提取系数，合并结果
        # ==========================================
        s6_t1 = Tex(r"提取 $y^k$ 的系数", tex_template=ctex, color=RED).next_to(s5_eq2, DOWN, buff=0.8)
        s6_t2 = Tex(r"令 $m + j = k \implies j = k - m$", tex_template=ctex, color=BLUE).next_to(s6_t1, DOWN, buff=0.5)
        
        self.play(FadeOut(s5_t2))
        self.play(Write(s6_t1))
        self.play(Write(s6_t2))
        self.wait(1.5)
        
        # 公式收缩坍塌合并
        s6_eq_final = MathTex(
            r"f(n,k) = \sum_{m=0}^k \binom{n+1}{m} (k+1-m)^n (-1)^m", 
            color=GOLD
        ).move_to(s5_eq2.get_center())
        s6_t_final = Tex("提取系数", tex_template=ctex, color=WHITE).scale(0.7).move_to(s6_t1.get_center())
        
        self.play(
            TransformMatchingShapes(s5_eq2, s6_eq_final),
            ReplacementTransform(s6_t1, s6_t_final),
            FadeOut(s6_t2)
        )
        self.wait(2.5)
        self.play(FadeOut(s6_eq_final), FadeOut(s6_t_final))

        # ==========================================
        # 第七段画面：最终结论及分布列
        # ==========================================
        s7_l1 = Tex(r"因为乙的出牌有 $n!$ 种全排列", tex_template=ctex, color=WHITE).move_to(UP * 1)
        self.play(Write(s7_l1))
        self.wait(1)
        
        s7_l2 = MathTex(r"P(X=k) = \frac{f(n,k)}{n!}", color=BLUE_A).next_to(s7_l1, DOWN, buff=0.8)
        self.play(Write(s7_l2))
        self.wait(1)
        
        # 最终展开
        s7_l3 = MathTex(r"P(X=k) = \frac{1}{n!} \sum_{m=0}^k \binom{n+1}{m} (-1)^m (k+1-m)^n", color=BLUE).move_to(s7_l2.get_center())
        self.play(ReplacementTransform(s7_l2, s7_l3))
        self.wait(1)
        
        # Q.E.D. 落幕
        qed_text = Tex("Q.E.D.", color=RED).scale(1.2).next_to(s7_l3, DOWN, buff=1)
        self.play(Write(qed_text))
        self.wait(3)
        
        # 全局淡出（可选）
        self.play(FadeOut(s7_l1), FadeOut(s7_l3), FadeOut(qed_text))