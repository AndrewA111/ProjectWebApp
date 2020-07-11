import static org.junit.Assert.*;

import org.junit.Test;

public class Tests {

	@Test
	public void addTest() {
		assertEquals("1 + 2 = 3", Calculator.add(1, 2), 3);
		assertEquals("10 + 2 = 12", Calculator.add(10, 2), 12);
	}
	
	@Test
	public void atobTest() {
		assertEquals("2 ^ 3 = 8", 8, Calculator.atob(2, 3), 0.01);
		assertEquals("100 ^ 0 = 1", 1, Calculator.atob(100, 0), 0.01);
		assertEquals("2 ^ (-1) = 0.5", 0.5, Calculator.atob(2, -1), 0.01);
	}

}
