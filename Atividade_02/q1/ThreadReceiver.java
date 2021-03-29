import java.io.*;
import java.net.*;
// import java.util.*;

public class ThreadReceiver extends Thread {
    // DataInputStream in;
    // Socket clientSocket;
    DatagramSocket dgramSocket = null;

    public ThreadReceiver(DatagramSocket dgramSocket) {
        try {
            this.dgramSocket = dgramSocket;
        } catch (Exception e) {
            // TODO: handle exception
        }
    }

    @Override
    public void run() {
        try {
             // cria um socket datagrama em uma porta especifica

            while (true) {
                byte[] buffer = new byte[1000]; // cria um buffer para receber requisições

                /* cria um pacote vazio */
                DatagramPacket dgramPacket = new DatagramPacket(buffer, buffer.length);
                this.dgramSocket.receive(dgramPacket); // aguarda a chegada de datagramas

                byte[] received = dgramPacket.getData();
                
                byte nickSize = received[0];
                
                byte[] nickByte = new byte[nickSize];
                System.arraycopy(received, 1, nickByte, 0, nickSize);
                String nick = new String(nickByte);

                byte msgSize = received[1+nickSize];
                byte[] msgByte = new byte[msgSize];
                System.arraycopy(received, 2 + nickSize, msgByte, 0, msgSize );
                String msg = new String(msgByte);

                System.out.println("Resposta do " + nick + ": " + msg );

            } // while
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        } finally {
            this.dgramSocket.close();
        }
    }
}