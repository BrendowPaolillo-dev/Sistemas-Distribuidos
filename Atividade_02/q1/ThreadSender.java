import java.io.*;
import java.net.*;
import java.util.*;

public class ThreadSender extends Thread {
    // DataOutputStream out;
    // Socket clientSocket;
    DatagramSocket dgramSocket;
    String resp;
    String nick;
    byte[] nickBytes;


    public ThreadSender(String nick, byte[] nickBytes, DatagramSocket dgramSocket) {
        try {
            this.dgramSocket = dgramSocket; //cria um socket datagrama
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

            System.out.println("IP Destino: ");
            String dstIP = reader.nextLine();
            int dstPort = 6666;
            
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

                System.out.println("Nova mensagem? (Y/N): ");
                this.resp = reader.nextLine();

            } while (this.resp.equals("N") || this.resp.equals("n") != true);

            /* libera o socket */
            this.dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        } //catch
    }
}