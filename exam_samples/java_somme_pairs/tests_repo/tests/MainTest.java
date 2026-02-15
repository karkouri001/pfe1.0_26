import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class MainTest {

    @Test
    void retourneZeroSiTableauNull() {
        assertEquals(0, Main.sommePairs(null));
    }

    @Test
    void retourneZeroSiTableauVide() {
        assertEquals(0, Main.sommePairs(new int[]{}));
    }

    @Test
    void additionneSeulementLesPairs() {
        assertEquals(6, Main.sommePairs(new int[]{1, 2, 3, 4, 5}));
    }

    @Test
    void retourneZeroSiAucunNombrePair() {
        assertEquals(0, Main.sommePairs(new int[]{1, 3, 5, 7, 9}));
    }

    @Test
    void gereNegatifsEtZero() {
        assertEquals(-8, Main.sommePairs(new int[]{-2, -3, -6, 1, 0}));
    }

    @Test
    void casMixteSupplementaire() {
        assertEquals(42, Main.sommePairs(new int[]{40, 1, 2, 4, -5, -4}));
    }
}
