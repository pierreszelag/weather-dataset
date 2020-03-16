import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import static java.util.Arrays.*;


public class frenchCities {
    ArrayList<ArrayList<String>> data = new ArrayList<ArrayList<String>>();
    ArrayList<String> sortedCities = new ArrayList<String>();
    ArrayList<String[]> citiesPop = new ArrayList<String[]>();

    public frenchCities() throws IOException {
        this.sortFrCities();
    }

    public static void main(String[] args) throws IOException {
        frenchCities test = new frenchCities();
    }

    public void sortFrCities() throws IOException {
        Scanner scanner = new Scanner(new File("villes_france.csv"));

        int maxPop = 0, maxIndex = 0;


        while (scanner.hasNextLine())
        {
            String[] line = scanner.nextLine().split(",");
            ArrayList<String> lineArray = new ArrayList<String>();
            lineArray.addAll(asList(line));
            data.add(lineArray);
        }
        scanner.close();

        while (this.sortedCities.size() < 3000) {
            for (int i = 0; i < this.data.size(); i++) {
                String number = this.data.get(i).get(14).replaceAll("\"","");
                Integer pop = Integer.valueOf(number);
                if (pop > maxPop){
                    maxIndex = i;
                    maxPop = pop;
                }
            }
            sortedCities.add(this.data.get(maxIndex).get(5));

            this.data.remove(maxIndex);
            maxPop = 0;
        }

        File myObj = new File("sortedcities.csv");
        FileWriter myWriter = new FileWriter("sortedcities3000.csv");

        for (String city: this.sortedCities){
            myWriter.write(city + ",\n");
        }

        myWriter.close();
    }
}
