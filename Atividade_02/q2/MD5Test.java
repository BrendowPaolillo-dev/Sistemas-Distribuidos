
public class MD5Test {



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
        return complete.digest();
    }

    public static void main(String[] args) {
        System.out.println("Md5Iniciado iniciado.");
        this.checksum();
    }
}