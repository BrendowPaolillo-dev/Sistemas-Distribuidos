import java.io.*;
import java.net.*;
import java.util.*;
import javax.swing.JOptionPane;

public class ThreadSender extends Thread {
    // DataOutputStream out;
    // Socket clientSocket;

    DatagramSocket dgramSocket;
    int resp = 0;
    String nick;
    byte[] nickBytes;


    public ThreadSender(String nick, byte[] nickBytes) {
        try {
            this.dgramSocket = new DatagramSocket(6666); //cria um socket datagrama
            this.nick = nick;
            this.nickBytes = nickBytes;

        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    @Override
    public void run(){

        try {
            Scanner reader = new Scanner(System.in);
            String dstIP = JOptionPane.showInputDialog("IP Destino?");
            int dstPort = Integer.parseInt(JOptionPane.showInputDialog("Porta Destino?"));
            
            /* armazena o IP do destino */
            InetAddress serverAddr = InetAddress.getByName(dstIP);
            int serverPort = dstPort; // porta do servidor

            do {
                byte[] nick = new byte[this.nickBytes.length];
                nick = this.nick.getBytes();


                System.out.println("Mensagem: ");
                String msg = reader.nextLine();

                byte[] m = msg.getBytes(); // transforma a mensagem em bytes
                byte[] mSize = new byte[] {(byte)m.length};


                byte[] packageToSend = new byte [this.nickBytes.length + nick.length + mSize.length + m.length];
                System.arraycopy(this.nickBytes, 0, packageToSend, 0, this.nickBytes.length);
                System.arraycopy(nick, 0, packageToSend, this.nickBytes.length, nick.length);
                System.arraycopy(mSize, 0, packageToSend, (this.nickBytes.length + nick.length), mSize.length);
                System.arraycopy(m, 0, packageToSend, (this.nickBytes.length + nick.length + mSize.length), m.length);

                // System.out.println(packageToSend.length);

                /* cria um pacote datagrama */
                DatagramPacket request
                        = new DatagramPacket(packageToSend, packageToSend.length, serverAddr, serverPort);

                /* envia o pacote */
                this.dgramSocket.send(request);

                /* cria um buffer vazio para receber datagramas */
                // byte[] buffer = new byte[1000];
                // DatagramPacket reply = new DatagramPacket(buffer, buffer.length);

                /* aguarda datagramas */
                // this.dgramSocket.receive(reply);
                // System.out.println("Resposta: " + new String(reply.getData(),0,reply.getLength()));

                resp = JOptionPane.showConfirmDialog(null, "Nova mensagem?", 
                        "Continuar", JOptionPane.YES_NO_OPTION);

            } while (resp != JOptionPane.NO_OPTION);

            /* libera o socket */
            this.dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        } //catch
    }
}