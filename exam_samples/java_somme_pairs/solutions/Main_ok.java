public class Main {
    public static int sommePairs(int[] valeurs) {
        if (valeurs == null) {
            return 0;
        }
        int somme = 0;
        for (int valeur : valeurs) {
            if (valeur % 2 == 0) {
                somme += valeur;
            }
        }
        return somme;
    }
}
