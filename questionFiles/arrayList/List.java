import java.util.Iterator;

public interface List<E> extends Iterable<E> {
	// Each List<E> object is a homogeneous list
	// whose elements are of type E.
	// ////////// Accessors ////////////
	public boolean isEmpty();

	// Return true if and only if this list is empty.
	public int size();

	// Return this list's length.
	public E get(int p);

	// Return the element at position p in this list.
	public boolean equals(List<E> that);

	// Return true if and only if this list and that have the
	// same length, and each element of this list equals
	// the corresponding element of that.
	
	
	// Return true if and only if object x is an element of this list
	public boolean contains(E x);
	
	// returns the index of object x in this list if it is an element, 
	// or �1 otherwise
	public int indexOf(E x);
	
	// return a new list that contains all of the elements in l with 
	// indices i through j-1
	public List<E> subList(int i, int j);
	
	// //////////Transformers ////////////
	public void clear();

	// Make this list empty.
	public void set(int p, E it);

	// Replace the element at position p in
	// this list by it.
	public void add(int p, E it);

	// Add it at position p in this list.
	public void addLast(E it);
	// Add it after the last element of this list.
	
	public void addAll (List<E> that);
	// Add all the elements of that after the
	// last element of this list.
	public E remove (int p);
	// Remove and return the element at
	// position p in this list.
	//////////// Iterator ////////////
	@Override
	public Iterator<E> iterator ();
	// Return an iterator that will visit all
	// elements of this list, in left-to-right order.

	


}
