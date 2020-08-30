import static org.junit.Assert.*;

import org.junit.Test;

public class Tests {

    @TestDescription (value = "Check that addition works")
    @TestHint (value = "+ hint")
	@Test
	public void addTest() {
		assertEquals("1 + 2 = 3", Calculator.add(1, 2), 3);
		assertEquals("10 + 2 = 12", Calculator.add(10, 2), 12);
	}

	@TestDescription (value = "Check subtraction works")
	@Test
	public void subtractionTest() {
		assertEquals("2 - 1 = 1", 1, Calculator.subtract(2, 1));
		assertEquals("5 - 10 = -5", -5, Calculator.subtract(5, 10));
	}

}
