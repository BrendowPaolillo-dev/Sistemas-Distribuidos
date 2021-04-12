import java.io.*;
import java.math.BigInteger;
import java.util.*;
import java.net.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.ByteBuffer;
import java.nio.file.Files;

public class UDPClient {

    DatagramSocket dgramSocket;
    DatagramPacket dgramPackage;
    int serverPort = 6666;
    InetAddress serverAddr;

    public UDPClient(){
        try {
            // Recebe o comandos
            System.out.println("UDPClient");
            Scanner reader = new Scanner(System.in);
            System.out.println("UDPClient2");

            //Cria socket de UDP
            this.dgramSocket = new DatagramSocket(this.serverPort);;
            
            /* armazena o IP do destino */
            System.out.println("IP Destino: ");
            String dstIP = "192.168.56.102";
            // se conecta com o servidor
            this.serverAddr = InetAddress.getByName(dstIP);

            run();

        } catch (Exception e) {
            // TODO: handle exception
        }
    }

    public StringBuilder convertToHexa(byte[] bytes){

        StringBuilder sb = new StringBuilder();
        
        // loop through the bytes array
        for (int i = 0; i < bytes.length; i++) {
            
            // the following line converts the decimal into
            // hexadecimal format and appends that to the
            // StringBuilder object
            sb.append(Integer
                    .toString((bytes[i] & 0xff) + 0x100, 16)
                    .substring(1));
        }

        return sb;
    }

    public String checksum(String fileName) throws Exception{
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

        StringBuilder sb = convertToHexa(complete.digest());
        
        return sb.toString();
    }

    // envia o pacote de dados para o servidor
    public void sendPackage (byte[] payload, int payloadSize){
        this.dgramPackage = new DatagramPacket(payload, payloadSize, this.serverAddr, this.serverPort);

        /* envia o pacote */
        try {
            this.dgramSocket.send(this.dgramPackage);
        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    public void splitFile(File f) throws IOException {
        
        int partCounter = 1;
        int sizeOfFiles = 1024;
        
        byte[] buffer = new byte[sizeOfFiles];

        String fileName = f.getName();

        if (fileName != null) {
            try (
                FileInputStream fis = new FileInputStream(f); 
                BufferedInputStream bis = new BufferedInputStream(fis)
            ) {
                String md5 = "";
                try {
                    //calcula o md5 do arquivo
                    md5 = checksum(fileName);   
                } catch (Exception e) {
                    //TODO: handle exception
                }
                
                System.out.println("Md5: " + md5);
                try {
                    Thread.sleep(100);
                    
                } catch (Exception e) {
                    //TODO: handle exception
                }
                //envia o md5 do arquivo total para o servidor
                byte[] byteArrayMd5 = md5.getBytes();
                sendPackage(byteArrayMd5, byteArrayMd5.length);
                
                //calcula a quantidade de pacotes a serem enviados
                long qtdOfPckg = (f.length()/buffer.length) + 1;
 
                System.out.println("Quantidade de pacotes: " + qtdOfPckg);
                
                //insere o Long no byte[]
                String qtdBuffer = String.valueOf(qtdOfPckg);
                try {
                    Thread.sleep(100);
                    
                } catch (Exception e) {
                    //TODO: handle exception
                }
                //envia o número de pacotes que o servidor deve ler
                sendPackage(qtdBuffer.getBytes(), qtdBuffer.getBytes().length);
                
                
                int bytesAmount = 0;
                while ((bytesAmount = bis.read(buffer)) > 0) {
                    try {
                        Thread.sleep(100);
                        
                    } catch (Exception e) {
                        //TODO: handle exception
                    }
                    sendPackage(buffer, bytesAmount);
                    System.out.println("payload: " + buffer);
    
                }
                System.out.println("Arquivo enviado com sucesso.");
            }
        } else {
            System.out.println("Não foi possível encontrar um arquivo com esse nome, digite um nome existente.");
        }
    }

    public void run() {

        Scanner reader = new Scanner(System.in);

        try {

            String resp = "";

            do {

                
                System.out.println("Digite o nome do arquivo e a extensão: ");
                String fileName = reader.nextLine();

                File f = new File(fileName);

                // transforma o nome do arquivo em bytes
                byte[] fileNameBytes = fileName.getBytes();
                // byte[] fileSize = new byte[32];

                // System.arraycopy(fileSize, 0, f.length(), 0, arg4);

                sendPackage(fileNameBytes, fileNameBytes.length);
                // sendPackage(, payloadSize);

                splitFile(f);

                System.out.println("Novo arquivo? (Y/N): ");
                resp = reader.nextLine();

            } while (resp.equals("N") || resp.equals("n") != true);

            /* libera o socket */
            dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        }

    }
    
    public static void main(String[] args) {
        System.out.println("Entrou");
        UDPClient client = new UDPClient();
    }
}
