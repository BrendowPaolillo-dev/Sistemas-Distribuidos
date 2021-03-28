
import java.io.*;
import java.net.*;
// import java.util.*;

public class ThreadReceiver extends Thread {
    // DataInputStream in;
    // Socket clientSocket;
    DatagramSocket dgramSocket = null;

    public ThreadReceiver() {
        try {
            this.dgramSocket = new DatagramSocket(6666);
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

                /* imprime e envia o datagrama de volta ao cliente */
                System.out.println("Cliente: " + new String(dgramPacket.getData(), 0, dgramPacket.getLength()));
                // DatagramPacket reply = new DatagramPacket(dgramPacket.getData(), dgramPacket.getLength(),
                //         dgramPacket.getAddress(), dgramPacket.getPort()); // cria um pacote com os dados

                // dgramSocket.send(reply); // envia o pacote
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