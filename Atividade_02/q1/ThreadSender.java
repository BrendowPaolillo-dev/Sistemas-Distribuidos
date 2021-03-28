
import java.io.*;
import java.net.*;
import java.util.*;
import javax.swing.JOptionPane;

public class ThreadSender extends Thread {
    // DataOutputStream out;
    // Socket clientSocket;

    DatagramSocket dgramSocket;
    int resp = 0;

    public ThreadSender() {
        try {
            this.dgramSocket = new DatagramSocket(6666); //cria um socket datagrama

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
                System.out.println("Mensagem: ");
                String msg = reader.nextLine();

                byte[] m = msg.getBytes(); // transforma a mensagem em bytes

                /* cria um pacote datagrama */
                DatagramPacket request
                        = new DatagramPacket(m, m.length, serverAddr, serverPort);

                /* envia o pacote */
                this.dgramSocket.send(request);

                /* cria um buffer vazio para receber datagramas */
                byte[] buffer = new byte[1000];
                DatagramPacket reply = new DatagramPacket(buffer, buffer.length);

                /* aguarda datagramas */
                this.dgramSocket.receive(reply);
                System.out.println("Resposta: " + new String(reply.getData(),0,reply.getLength()));

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