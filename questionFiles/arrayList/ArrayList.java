import java.util.Iterator;
import java.util.NoSuchElementException;

public class ArrayList<E> implements List<E> {
	private E[] elems;
	private int size;

	// ////////// Constructor ////////////
	@SuppressWarnings("unchecked")
	public ArrayList(int cap) {
		elems = (E[]) new Object[cap];
		size = 0;
	}
	
	public ArrayList(){
		this(10);
	}

	@Override
	public boolean isEmpty() {

		return (size == 0);
	}

	@Override
	public int size() {
		return size;
	}

	// Return the element at position p in this list.
	@Override
	public E get(int p) {
		if (p < 0 || p >= size)
			throw new NoSuchElementException();
		return elems[p];

	}

	// Return true if and only if this list and that have the
	// same length, and each element of this list equals
	// the corresponding element of that.
	@Override
	public boolean equals(List<E> that) {
		if (that.size() != size)
			return false;
		for (int i = 0; i < size; i++) {
			if (!this.get(i).equals(that.get(i)))
				return false;
		}
		return true;
	}
	
	// Return true if and only if object x is an element of this list
	public boolean contains(E x) {
		
//		for(E elem : this.elems) {
//			if (elem.equals(x)){
//				return true;
//			}	
//		}	
		
		for(int i = 0; i < this.elems.length; i ++) {
			if(elems[i] != null) {
				if ( elems[i].equals(x)) {
					return true;
				}
			}
			
		}
		
		return false;
	}
	
	// returns the index of object x in this list if it is an element, 
	// or �1 otherwise
	public int indexOf(E x) {
		
		for(int i = 0; i < this.elems.length; i ++) {
			if(elems[i] != null) {
				if ( elems[i].equals(x)) {
					return i;
				}
			}
			
		}
		
		return -1;
	}
	
	// return a new list that contains all of the elements in l with 
	// indices i through j�1
	public List<E> subList(int i, int j){
		
		List<E> temp = new ArrayList<E>();
		
		for(int n = i; n < j; n++) {
			temp.addLast(elems[n]);
		}
		
		return temp;
	}

	// Make this list empty.
	@Override
	public void clear() {
		size = 0;

	}

	// Replace the element at position p in
	// this list by it.
	@Override
	public void set(int p, E it) {
		if (p < 0 || p >= size)
			throw new NoSuchElementException();
		else
			elems[p] = it;

	}

	// Add it at position p in this list
	// if no room, double size of the array
	@Override
	public void add(int p, E it) {
		if(size==elems.length) this.doubleArray(); 
		for (int i = size; i >= p; i--)
			elems[i + 1] = elems[i];
		elems[p] = it;
		size++;

	}

	// Add it after the last element of this list.
	@Override
	public void addLast(E it) {
		if(this.size == elems.length) {
			this.overflow();
		}
		
		elems[size++] = it;

	}

	// Add all the elements of that after the
	// last element of this list.
	@Override
	public void addAll(List<E> that) {
		int newCapacity = this.size() + that.size();
		while (elems.length < newCapacity)
			doubleArray();
		for (int j = 0; j < that.size(); j++)
			elems[size + j] = that.get(j);
	}

	public E[] getElems() {
		return elems;
	}

	public void setElems(E[] elems) {
		this.elems = elems;
	}

	public int getSize() {
		return size;
	}

	public void setSize(int size) {
		this.size = size;
	}
	
	public void overflow() {
		
		E[] temp = (E[]) new Object[2 * elems.length];
		
		for(int i = 0; i < elems.length; i++) {
			temp[i] = elems[i];
		}
		
		this.elems = temp;
	}

	// Remove and return the element at
	// position p in this list.
	@Override
	public E remove(int p) {
		E val = elems[p];
		for (int i = p + 1; i < size; i++)
			elems[i] = elems[i + 1];
		size--;
		return val;
	}

	// return an iterator that will visit all
	// elements of this list, in left-to-right order.
	@Override
	public Iterator<E> iterator() {
		return new LRIterator();
	}

	// //////////Inner class ////////////
	private class LRIterator implements Iterator<E> {
		private int position;

		// position is the index of the slot containing the
		// next element to be visited.
		private LRIterator() {
			position = 0;
		}

		@Override
		public boolean hasNext() {
			return (position < size);
		}

		@Override
		public E next() {
			if (position >= size)
				throw new NoSuchElementException();
			return elems[position++];
		}

		@Override
		public void remove() {
			// omitting this one

		}

	}

	public void doubleArray() {
		int doub = 2 * elems.length;
		@SuppressWarnings("unchecked")
		E[] newElems = (E[]) new Object[doub];
		for (int i = 0; i < size; i++)
			newElems[i] = elems[i];
		elems = newElems;
	}
	
}
