import java.io.*;
import java.util.*;
import java.net.*;


public class UDPClient {
    
    public static void splitFile(File f, DatagramSocket dgramSocket) throws IOException {
        int partCounter = 1;

        int sizeOfFiles = 1024;// 1MB
        byte[] buffer = new byte[sizeOfFiles];

        String fileName = f.getName();

        //try-with-resources to ensure closing stream
        try (FileInputStream fis = new FileInputStream(f);
             BufferedInputStream bis = new BufferedInputStream(fis)) {

            int bytesAmount = 0;
            while ((bytesAmount = bis.read(buffer)) > 0) {

                //write each chunk of data into separate file with different number in name
                // String filePartName = String.format("%s.%03d", fileName, partCounter++);
                // File newFile = new File(f.getParent(), filePartName);
                // try (FileOutputStream out = new FileOutputStream(newFile)) {
                //     out.write(buffer, 0, bytesAmount);
                // }
            }
        }
    }
    public static void main(String args[]) {
        
        Scanner reader = new Scanner(System.in);
        
        try {
            System.out.println("IP Destino: ");
            String dstIP = reader.nextLine();
            int dstPort = 6666;
            
            /* armazena o IP do destino */
            InetAddress serverAddr = InetAddress.getByName(dstIP);

            DatagramSocket dgramSocket = new DatagramSocket(dstPort);
            
            String resp = "";

            do {
     
                System.out.println("Digite o nome do arquivo e a extensao: ");
                String fileName = reader.nextLine();

                byte[] fileNameBytes = fileName.getBytes(); // transforma o nome do arquivo em bytes

                /* cria um pacote datagrama */
                DatagramPacket request
                        = new DatagramPacket(fileNameBytes, fileNameBytes.length, serverAddr, dstPort);

                /* envia o pacote */
                dgramSocket.send(request);

                splitFile(new File(fileName), dgramSocket);
                
                System.out.println("Novo arquivo? (Y/N): ");
                resp = reader.nextLine();

            } while (resp.equals("N") || resp.equals("n") != true);

            /* libera o socket */
            dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        } //catch



    } //main	
}
