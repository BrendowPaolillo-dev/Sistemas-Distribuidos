import java.io.*;
import java.net.*;
import java.security.MessageDigest;

public class UDPServer {
    DatagramSocket dgramSocket;
    byte[] buffer;
    DatagramPacket dgramPacket;

    public UDPServer() {
        try {
            this.dgramSocket = new DatagramSocket(6666);
        } catch (Exception e) {
            //TODO: handle exception
        }
        this.buffer = new byte[1024]; // cria um buffer para receber requisições
        this.dgramPacket = new DatagramPacket(buffer, buffer.length);
        
        run();
    }

    public byte[] checksum(String fileName) throws Exception{
        InputStream fis =  new FileInputStream(fileName);

        byte[] buffer = new byte[1024];
        MessageDigest complete = MessageDigest.getInstance("MD5");
        int numRead;

        do {
            numRead = fis.read(buffer);
            if (numRead > 0) {
                complete.update(buffer, 0, numRead);
            }
        } while (numRead != -1);

        fis.close();
        return complete.digest();
    }

    public void run(){
        try {
            // cria um socket datagrama em uma porta especifica
            
            try {
                this.dgramSocket.receive(this.dgramPacket); // aguarda a chegada de datagramas
 
                byte[] fileNameBytes = this.dgramPacket.getData();
                String fileName = new String(fileNameBytes);
                System.out.println("Nome do arquivo: " + fileName);
                
                byte[] file = new byte[1024];
                
                if (fileName != null)
                try {
                    byte[] md5Real = this.dgramPacket.getData();
                    byte[] md5Calc = new byte[1024];
                    while (md5Calc != md5Real) {
                        //recebe a carga de dados do UDP
                        byte[] payload = this.dgramPacket.getData();

                        //concatena a carga recebida no vetor do arquivo completo
                        System.arraycopy(payload, 0, file, file.length, file.length + payload.length);
                        
                        //preenche o arquivo
                        File newFile = new File(fileName);
                        try (FileOutputStream out = new FileOutputStream(newFile)) {
                            out.write(file);
                        }

                        //calcula toda vez o md5
                        md5Calc = checksum(fileName);
        
                } // while
                System.out.println("Arquivo recebido com sucesso.");
                } catch (Exception e) {
                    //TODO: handle exception
                }
           } catch (SocketException e) {
               System.out.println("Socket: " + e.getMessage());
           } catch (IOException e) {
               System.out.println("IO: " + e.getMessage());
           } finally {
               dgramSocket.close();
           }
        } catch (Exception e) {
            //TODO: handle exception
        }
        System.out.println("Finalizada a transferência.");
    }

    public static void main(String[] args) {
        UDPServer server = new UDPServer();
    }
}
