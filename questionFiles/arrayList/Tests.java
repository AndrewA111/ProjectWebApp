import static org.junit.Assert.*;

import org.junit.Test;

public class Tests {

	@Test
	public void addedTest() {
		List<Integer> list = new ArrayList<Integer>();
		
		list.add(0,1);
		list.add(0, 2);
		list.add(0, 4);
		
		assertEquals("add(0,1) should add 1 to list", true, list.contains(1));
		assertEquals("add(0,4) should add 1 to list", true, list.contains(4));
	}
	

	@Test
	public void failureTest() {
		List<Integer> list = new ArrayList<Integer>();
		
		assertEquals("Purposeful test failure", true, list.contains(3));
	}

}
