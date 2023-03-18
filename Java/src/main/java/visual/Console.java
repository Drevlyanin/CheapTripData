package visual;

import javax.swing.*;
import javax.swing.border.Border;
import java.awt.*;
import java.io.IOException;
import java.io.OutputStream;

public class Console extends OutputStream {

    JFrame consoleFrame;

    JPanel panel;
    JTextArea textArea;

    ScrollPane pane;

    public Console () {
        consoleFrame = new JFrame("Console");
        textArea = new JTextArea();
        panel = new JPanel();
        pane = new ScrollPane();

        Border border = BorderFactory.createEtchedBorder();

        pane.add(textArea);

        panel.add(pane);
        pane.setPreferredSize(new Dimension(500,400));
        panel.setBorder(BorderFactory.createEmptyBorder(30,30,30,30));
        panel.setBorder(border);

        consoleFrame.add(panel);
        consoleFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        consoleFrame.setBounds(600, 60, 40, 40);
        consoleFrame.pack();
        consoleFrame.setVisible(true);
    }

    @Override
    public void write(int b) throws IOException {
        textArea.append(String.valueOf((char) b));
        textArea.setCaretPosition(textArea.getDocument().getLength());
        textArea.update(textArea.getGraphics());
    }
}
