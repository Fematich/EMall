import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

import org.wltea.analyzer.core.IKSegmenter;
import org.wltea.analyzer.core.Lexeme;

public class Segmenter {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public List<String> segment(String text) throws IOException {
	     IKSegmenter segmenter = new IKSegmenter(new StringReader(text),true);
	     Lexeme t=new Lexeme(0,0,0,0);
	     t=segmenter.next();
	     List<String> ret = new ArrayList<String>();
	     while (t!=null) {
	    	 ret.add(t.getLexemeText());
	    	 //System.out.println(t.getLexemeText());
	    	 t=segmenter.next();
	      }
		return ret;
	}
	public String tokenize(String text) throws IOException {
	     IKSegmenter segmenter = new IKSegmenter(new StringReader(text),true);
	     Lexeme t=new Lexeme(0,0,0,0);
	     t=segmenter.next();
	     String ret = new String();
	     while (t!=null) {
	    	 ret+=' '+t.getLexemeText();
	    	 //System.out.println(t.getLexemeText());
	    	 t=segmenter.next();
	      }
		return ret;
	}
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
	      IKSegmenter segmenter = new IKSegmenter(new StringReader("提摩尔湖厚厚的冰层开始化解，融下的冰渣在湖面翻滚，发出沙哑的挣扎。 黎明第一缕阳光，是吸血鬼永生的终结。 黎明第一缕阳光，是人类最坚强的希望。 黎明第一缕阳光，是大自然的深情呼吸。 2004年8月3日星期二 洒脱就是没有留下一丝遗憾。或许是月夜下的城堡延续了过多的沧桑，当蝙蝠扇动带血的双翼，飞出遍布裂痕的古老钟楼时，吸血鬼的獠牙翻出嘴唇，贪婪的吮吸空气中传来的血腥的味道。嗜杀的冲动激荡着最后的理智。 不管成功失败，吸血鬼的行动只有前进。 兰斯大教堂的钟声再次响起，来自圣经的祝福随着每一丝跳动的空气，净化着坚强搏动的心。已经太久太久没享受过洛丁山脉斯朗格峰顶年毫无掩饰的阳光。已经有太久太久没听过提摩尔湖那温柔的回味。人类，到了坚强抗击的时刻了。 风吹过卡里石窟的岩洞，擦去带着本味的跌宕。每一天的日出，是大地的呼唤。卷起精灵的触手拨开沉沉的湿汽。每一天的日落，却泛着淡淡的失落。如此年复一年，直到找回属于大地精灵之角的力量。 战争可以延续漫长的岁月，直到淡化种族、历史、仇恨、爱情。。。直到剩下麻木的杀戮。 天下第一武道会竞技场在淡淡的晨曦中，散去浓雾。 为了“天下第一”，埃斯洛尼安这片大陆的强者，再次汇聚在这块象征荣誉与辉煌的土地上。 13：00 第一场 浪漫战队（人类） VS 天炼英雄（吸血鬼） 这场比赛让埃斯洛尼安大陆的人深深记住了一个教训。 一分钟的时间，可以决定一个种族的命运。 在烟花绚丽的那一刻，骄傲的吸血鬼轻轻擦去嘴角残留的血液，每个人（鬼？）都在盘算自己的进攻方式。希望用压倒性的战斗气势迅速掌握节奏。 人类低头无语。枪手们在最后计算炮火支援的弹道，摩尔连射的穿透力会让这群高傲的先生们知道，兵无定式！ 战斗打响了，随着迷雾的扩散迅速将整个竞技场的空气燃烧。天空开始出现班驳的裂痕，大块的陨石从天而降，砸向人类。 这离比赛开始才不过39秒。 人类并没有慌乱。法师迅速的展开魔法结界，原本阴郁的天空也被魔法的光茫闪烁的晶亮。顽强的抵抗在坚持。 吸血鬼的攻势被硬生生的遏制住了。人类开始反攻。 硝烟散去，几个伤痕累累的枪手扶起因为魔法的反噬而虚脱的法师走下竞技场。 身后是吸血鬼的遗憾。 13：05 浪漫战队 人胜 日升光明、月揽黑夜。从天地诞生的那一天起，黑与白这对孪生兄弟就如影随形般交替在这个永恒的世界里。守护自己的无尽。 17：30 第二场 浪漫菜鸟无双队（人类） VS 嗜血同盟（吸血鬼） 赛事尚未开始，场上的气氛确是达到了濒临崩溃的界点。 人类依靠紧密的团结阵势得到了连续的胜利，此时此刻，天性的贪婪慢慢侵吞了人类的思维。对于胜利，不光是人类，就连吸血鬼和魔灵都不会将其拒之门外。 至于接连的挫败，同时也狠狠激怒了高傲的吸血鬼。这些来自月夜的黑暗强者，可以失去永生的躯体，但是无法忍受柔弱的刺激。 “月姐，我们会赢的！” 坚强的战士对队友也是对自己说。 人类开始观察吸血鬼，交换着眼神，传递作战计划。 （其间发生了好多精彩花絮，请关注天之炼狱官网相关报道） 吸血鬼深深的吸了口气，不能再辱没吸血鬼一族的强大了。"),true);
	      //System.out.println(segmenter.toString());
	      Lexeme t=new Lexeme(0,0,0,0);
	      t=segmenter.next();
	      while (t!=null) {
	    	  	System.out.println(t.getLexemeText());
	    	  	t=segmenter.next();
	        }
	      
	      
	}
	
}
