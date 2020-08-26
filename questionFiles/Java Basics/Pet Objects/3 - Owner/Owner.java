// import required to use ArrayList
import java.util.ArrayList;

public class Owner {
	
	// owner's name
	private String name;
	
	/*
	 * List of pets
	 * 
	 * Note generic type '<Pet>'
	 * 
	 * Note: import statement at top of page
	 */
	private ArrayList<Pet> petList;
	
	// constructor
	public Owner(String name) {
		
		// set name
		this.name = name;
		
		/*
		 * create an empty ArrayList
         */
	}
	W
	/*
	 * complete the addPet method to add
	 * a pet to this owner's pet list
	 */
	public void addPet(Pet p) {

	}
	
	/*
	 * Getters
	 */

	public String getName() {
		return name;
	}

	public ArrayList<Pet> getPetList() {
		return petList;
	}
	
	

}
