package syc;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import javax.imageio.ImageIO;

public class HomePage extends JFrame {
	static String host;
	static String user;
	static String password;
	private JPanel topPanel;
	private JPanel centerPanel;
	private JPanel clPanel;
	private JPanel crPanel;
	private JLabel jLabelSelectedPic;
	private JButton selectPic;
	private JButton proRetr32;
	private JButton proRetr16;
	private String selectedFilePath;
	private List<String> ninePics;
	public HomePage() {
		JPanel p=new JPanel() {
			protected void paintComponent(Graphics g) {
				super.paintComponent(g);
				Image backGround=new ImageIcon("./picture/background.jpg").getImage();
				g.drawImage(backGround, 0, 0, this.getWidth(), this.getHeight(), this);
			}
		};
		setContentPane(p);
		p.setLayout(new GridBagLayout());
		createTopPanel();
		createCenterPanel();
		//set topPanel
		GridBagConstraints c1=new GridBagConstraints();
		c1.gridx=0;
		c1.gridy=0;
		c1.weightx=1.0;
		c1.weighty=0.2;
		c1.fill=GridBagConstraints.BOTH;
		p.add(topPanel,c1);
		//set centerPanel
		GridBagConstraints c2=new GridBagConstraints();
		c2.gridx=0;
		c2.gridy=1;
		c2.ipady=350;
		c2.weightx=1;
		c2.weighty=0.8;
		c2.fill=GridBagConstraints.BOTH;
		p.add(centerPanel,c2);
	}
	void createTopPanel() {
		topPanel=new JPanel();
		topPanel.setLayout(new BoxLayout(topPanel,BoxLayout.X_AXIS));
		topPanel.add(Box.createHorizontalStrut(50));
		Image img=new ImageIcon("./picture/uestc.jpg").getImage();
		img=img.getScaledInstance(100, 100, Image.SCALE_DEFAULT);
		JLabel uestc= new JLabel(new ImageIcon(img));
		topPanel.add(uestc);
		topPanel.add(Box.createHorizontalStrut(70));
		JLabel title=new JLabel("YaleFace Dataset Recognition");
		title.setFont(new Font("Verdana",Font.BOLD,36));
		topPanel.add(title);
		topPanel.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));
	}
	void createCenterPanel() {
		centerPanel=new JPanel();
		centerPanel.setLayout(new BorderLayout());
		createCLPanel();
		createCRPanel();
		clPanel.setPreferredSize(new Dimension(270,centerPanel.getHeight()));
		crPanel.setPreferredSize(new Dimension(centerPanel.getWidth()-270,centerPanel.getHeight()));
		centerPanel.add(clPanel,BorderLayout.WEST);
		centerPanel.add(crPanel,BorderLayout.CENTER);
	}
	void createCLPanel() {
		clPanel=new JPanel();
		clPanel.setLayout(new BorderLayout());
		selectPic=new JButton("Select Photo");
		selectPic.setFont(new Font("Î¢ÈíÑÅºÚ", Font.BOLD, 22));
		selectPic.setFocusPainted(false);
		selectPic.addActionListener(new selectAction());
		clPanel.add(selectPic,BorderLayout.NORTH);
		JPanel clbPanel=new JPanel();
		clbPanel.setLayout(new FlowLayout());
		clbPanel.setPreferredSize(new Dimension(clPanel.getWidth(),75));
		proRetr32=new JButton("Face Recognition(32bit)");
		proRetr32.setFont(new Font("Î¢ÈíÑÅºÚ",Font.BOLD,20));
		proRetr32.setBorder(BorderFactory.createLoweredBevelBorder());
		proRetr32.setVisible(false);
		proRetr32.addActionListener(new retrieve32Action());
		clbPanel.add(proRetr32);
		proRetr16=new JButton("Face Recognition(16bit)");
		proRetr16.setFont(new Font("Î¢ÈíÑÅºÚ",Font.BOLD,20));
		proRetr16.addActionListener(new retrieve16Action());
		proRetr16.setBorder(BorderFactory.createLoweredBevelBorder());
		proRetr16.setVisible(false);
		clbPanel.add(proRetr16);
		clbPanel.setPreferredSize(new Dimension(clPanel.getWidth()-20,100));
		clbPanel.setBorder(BorderFactory.createEmptyBorder(0,5,0,5));
		clPanel.add(clbPanel,BorderLayout.SOUTH);
		
		jLabelSelectedPic=new JLabel();
		jLabelSelectedPic.setBorder(BorderFactory.createEmptyBorder(5,20,5,5));
		clPanel.add(jLabelSelectedPic,BorderLayout.CENTER);
		clPanel.setBorder(BorderFactory.createEmptyBorder(0,5,0,5));
	}
	void createCRPanel() {
		crPanel=new JPanel();
		crPanel.setBorder(BorderFactory.createLineBorder(Color.BLACK, 3));
	}
	void showNinePics() {//
		crPanel.removeAll();
		crPanel.setLayout(new GridLayout(3,3,5,5));
		for(int i=0;i<9;++i) {
			Image img=null;
			try {
				img=ImageIO.read(new File(ninePics.get(i)));
			}catch(IOException ex) {
				int a=1;
			}
			img=img.getScaledInstance(crPanel.getWidth()/3-10, crPanel.getHeight()/3-10, Image.SCALE_DEFAULT);
			ImageIcon imgIcon=new ImageIcon(img);
			JLabel label=new JLabel(imgIcon);
			label.setBorder(BorderFactory.createLineBorder(Color.BLACK, 3));
			crPanel.add(label);
		}
		crPanel.validate();
	}
	class selectAction implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			JFileChooser jfc=new JFileChooser();
		    jfc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES );
		    jfc.showDialog(new JLabel(), "Ñ¡Ôñ");
		    File file=jfc.getSelectedFile();
		    selectedFilePath=file.getAbsolutePath();
		    Image img=null;
		    try {
			    img=ImageIO.read(new File(selectedFilePath));
		    }catch(IOException ex) {}
		    img=img.getScaledInstance(220, 220, Image.SCALE_DEFAULT);
		    ImageIcon imgIcon=new ImageIcon(img);
		    jLabelSelectedPic.setIcon(imgIcon);
		    proRetr32.setVisible(true);
		    proRetr16.setVisible(true);

		}
	}
	class retrieve32Action implements ActionListener{
		public void actionPerformed(ActionEvent e) {
			File dir=new File("");
			String[] args=new String[] {"python",dir.getAbsolutePath()+"\\retrieveNearestPics32.py",selectedFilePath,host,user,password};
			ninePics=new ArrayList<>();
			try {
				Process proc=Runtime.getRuntime().exec(args);
				BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
				String line = null;
				while((line=in.readLine())!=null) {
					ninePics.add(line);
				}
				in.close();
				proc.waitFor();
			}catch (IOException err) {
	            err.printStackTrace();
	        } catch (InterruptedException err) {
	            err.printStackTrace();
	        } 
			showNinePics();
			
		}
	}
	class retrieve16Action implements ActionListener{
		public void actionPerformed(ActionEvent e) {
			File dir=new File("");
			String[] args=new String[] {"python",dir.getAbsoluteFile()+"\\retrieveNearestPics16.py",selectedFilePath,host,user,password};
			ninePics=new ArrayList();
			try {
				Process proc=Runtime.getRuntime().exec(args);
				BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
				String line = null;
				while((line=in.readLine())!=null) {
					ninePics.add(line);
				}
				in.close();
				proc.waitFor();
			}catch(IOException err) {
				err.printStackTrace();
			}catch(InterruptedException err) {
				err.printStackTrace();
			}
			showNinePics();
		}
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		host=args[0];
		user=args[1];
		password=args[2];
		File dir=new File("");
		String[] arg=new String[] {"python",dir.getAbsolutePath()+"\\loadHashCodes.py",host,user,password};
		try {
			Process proc=Runtime.getRuntime().exec(arg);
			proc.waitFor();
		}catch (IOException err) {
            err.printStackTrace();
        } catch (InterruptedException err) {
            err.printStackTrace();
        } 
		
		HomePage frame=new HomePage();
		frame.setTitle("ÈËÁ³Ê¶±ðÏµÍ³");
		int x=Toolkit.getDefaultToolkit().getScreenSize().width/4;
		int y=Toolkit.getDefaultToolkit().getScreenSize().height/4;
		frame.setSize(960,640);//¿ØÖÆ´°¿Ú´óÐ¡
		frame.setLocation(x,y);
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

	}

}
