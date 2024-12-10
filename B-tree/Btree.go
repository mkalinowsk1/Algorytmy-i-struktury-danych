package main

import (
	"encoding/binary"
	"fmt"
	"os"
)

const (
	order      = 3
	nodeSize   = 4096
	headerSize = 4
)

type Node struct {
	keys  []int
	child []*Node
	n     int
	t     int
	leaf  bool
}

type BTree struct {
	t       int
	root    *Node
	file    *os.File
	RootPos int64
}

func createNode(t int, leaf bool) *Node {
	return &Node{
		keys:  make([]int, 2*t-1),
		child: make([]*Node, 2*t),
		leaf:  leaf,
		n:     0,
		t:     t,
	}
}

func (b *BTree) insert(k int) {
	if b.root == nil {
		b.root = createNode(b.t, true)
		b.root.keys[0] = k
		b.root.n = 1
		b.writeNode(b.root)
		b.RootPos = 0
	} else {
		if b.root.n == 2*b.t-1 {
			s := createNode(b.t, false)
			s.child[0] = b.root
			s.split(0, b.root)
			i := 0
			if s.keys[0] < k {
				i++
			}
			s.child[i].insertNonFull(k)
			b.root = s
			b.writeNode(b.root)
			b.RootPos = 0
		} else {
			b.root.insertNonFull(k)
			b.writeNode(b.root)
		}
	}
}

func (node *Node) insertNonFull(k int) {
	i := node.n - 1
	if node.leaf == true {
		for i >= 0 && node.keys[i] > k {
			node.keys[i+1] = node.keys[i]
			i--
		}
		node.keys[i+1] = k
		node.n++
	} else {
		for i >= 0 && node.keys[i] > k {
			i--
		}
		if node.child[i+1].n == 2*node.t-1 {
			node.split(i+1, node.child[i+1])
			if node.keys[i+1] < k {
				i++
			}
		}
		node.child[i+1].insertNonFull(k)
	}
}

func (node *Node) split(i int, y *Node) {
	var z *Node = createNode(y.t, y.leaf)
	z.n = node.t - 1

	for j := 0; j < node.t-1; j++ {
		z.keys[j] = y.keys[j+node.t]
	}

	if y.leaf == false {
		for j := 0; j < node.t; j++ {
			z.child[j] = y.child[j+node.t]
		}
	}
	y.n = node.t - 1
	for j := node.n; j >= i+1; j-- {
		node.child[j+1] = node.child[j]
	}
	node.child[i+1] = z
	for j := node.n - 1; j >= i; j-- {
		node.keys[j+1] = node.keys[j]
	}
	node.keys[i] = y.keys[node.t-1]
	node.n++
}

func (node *Node) search(k int) bool {
	i := 0
	for i < node.n && k > node.keys[i] {
		i++
	}
	if node.keys[i] == k {
		return true
	}
	if node.leaf == true {
		return false
	}
	return node.child[i].search(k)
}

func (node *Node) findKey(k int) int {
	idx := 0
	for idx < node.n && node.keys[idx] < k {
		idx++
	}
	return idx
}

func (node *Node) delete(k int) {
	fmt.Print("del")
	idx := node.findKey(k)

	if idx < node.n && node.keys[idx] == k {
		if node.leaf {
			node.removeFromLeaf(idx)
		} else {
			node.removeFromNonLeaf(idx)
		}
	} else {
		if node.leaf {
			fmt.Println("key: ", k, " does not exist")
			return
		}
	}

	flag := idx == node.n

	if node.child[idx].n < node.t {
		node.fill(idx)
	}

	if flag && idx > node.n {
		node.child[idx-1].delete(k)
	} else {
		node.child[idx].delete(k)
	}
	return

}

func (node *Node) removeFromLeaf(idx int) {
	for i := idx + 1; i < node.n; i++ {
		node.keys[i-1] = node.keys[i]
	}
	node.n--
	return
}

func (node *Node) removeFromNonLeaf(idx int) {
	fmt.Print("frnolef")
	k := node.keys[idx]

	if node.child[idx].n >= node.t {
		pred := node.getPredecessor(idx)
		node.keys[idx] = pred
		node.child[idx].delete(pred)
	} else if node.child[idx+1].n >= node.t {
		succ := node.getSuccessor(idx)
		node.keys[idx] = succ
		node.child[idx+1].delete(succ)
	} else {
		node.merge(idx)
		node.child[idx].delete(k)
	}
	return
}

func (node *Node) getPredecessor(idx int) int {
	fmt.Print("getpred")
	cur := node.child[idx]
	for !cur.leaf {
		cur = cur.child[cur.n]
	}
	return cur.keys[cur.n-1]
}

func (node *Node) getSuccessor(idx int) int {
	fmt.Print("getsucc")
	cur := node.child[idx+1]
	for !cur.leaf {
		cur = cur.child[0]
	}
	return cur.keys[0]
}

func (node *Node) fill(idx int) {
	fmt.Print("fill")
	if idx != 0 && node.child[idx-1].n >= node.t {
		node.borrowFromPrev(idx)
	} else if idx != node.n && node.child[idx+1].n >= node.t {
		node.borrowFromNext(idx)
	} else {
		if idx != node.n {
			node.merge(idx)
		} else {
			node.merge(idx - 1)
		}
		return
	}
}

func (node *Node) borrowFromPrev(idx int) {
	fmt.Print("borrowfp")
	child := node.child[idx]
	sibling := node.child[idx-1]

	for i := child.n - 1; i >= 0; i-- {
		child.keys[i+1] = child.keys[i]
	}

	if !child.leaf {
		for i := child.n; i >= 0; i-- {
			child.child[i+1] = child.child[i]
		}
	}

	child.keys[0] = node.keys[idx-1]

	if !child.leaf {
		child.child[0] = sibling.child[sibling.n]
	}

	node.keys[idx-1] = sibling.keys[sibling.n-1]

	child.n++
	sibling.n--

	return
}

func (node *Node) borrowFromNext(idx int) {
	fmt.Print("borfn")
	child := node.child[idx]
	sibling := node.child[idx+1]

	child.keys[child.n] = node.keys[idx]

	if !child.leaf {
		child.child[child.n+1] = sibling.child[0]
	}
	node.keys[idx] = sibling.keys[0]

	for i := 1; i < sibling.n; i++ {
		sibling.keys[i-1] = sibling.keys[i]
	}

	if !sibling.leaf {
		for i := 1; i <= sibling.n; i++ {
			sibling.child[i-1] = sibling.child[i]
		}
	}
	child.n++
	sibling.n--

	return
}

func (node *Node) merge(idx int) {
	fmt.Print("merge")
	child := node.child[idx]
	sibling := node.child[idx+1]

	child.keys[node.t-1] = node.keys[idx]

	for i := 0; i < sibling.n; i++ {
		child.keys[i+node.t] = sibling.keys[i]
	}

	if !child.leaf {
		for i := 0; i <= sibling.n; i++ {
			child.child[i+node.t] = sibling.child[i]
		}
	}

	for i := idx + 1; i < node.n; i++ {
		node.keys[i-1] = node.keys[i]
	}

	for i := idx + 2; i <= node.n; i++ {
		node.child[i-1] = node.child[i]
	}

	child.n += sibling.n + 1
	node.n--

	sibling = nil
	return
}

func (b *BTree) delete(k int) {
	if b.root == nil {
		fmt.Println("tree is empty")
		return
	}

	b.root.delete(k)

	if b.root.n == 0 {
		if b.root.leaf {
			b.root = nil
		} else {
			b.root = b.root.child[0]
		}
	}
	return
}

func (b *BTree) writeNode(node *Node) {

	pos := b.rootPos(node)
	b.file.Seek(pos, 0)

	data := nodeToBytes(node)
	b.file.Write(data)
}

func nodeToBytes(node *Node) []byte {
	data := make([]byte, len(node.keys)*4)
	for i := 0; i < len(node.keys); i++ {
		binary.LittleEndian.PutUint32(data[i*4:], uint32(node.keys[i]))
	}
	return data
}

func (b *BTree) rootPos(node *Node) int64 {
	return int64(headerSize + nodeSize*node.n)
}

func (b *BTree) readNode(pos int64) (*Node, error) {

	_, err := b.file.Seek(pos, 0)
	if err != nil {
		return nil, err
	}

	data := make([]byte, nodeSize)
	_, err = b.file.Read(data)
	if err != nil {
		return nil, err
	}

	return bytesToNode(data)
}

func bytesToNode(data []byte) (*Node, error) {

	keys := make([]int, len(data)/4)
	for i := 0; i < len(keys); i++ {
		keys[i] = int(binary.LittleEndian.Uint32(data[i*4 : (i+1)*4]))
	}

	node := &Node{
		keys: make([]int, len(keys)),
		n:    len(keys),
	}
	copy(node.keys, keys)
	return node, nil
}

func (b *BTree) printTree() {
	if b.root == nil {
		fmt.Println("Empty tree")
		return
	}
	b.root.traverse(0)
}

func (node *Node) traverse(indent int) {
	var i int
	for i = 0; i < node.n; i++ {
		if !node.leaf {
			node.child[i].traverse(indent + 4)
		}
		for j := 0; j < indent; j++ {
			fmt.Print(" ")
		}
		fmt.Println(node.keys[i])
	}
	if !node.leaf {
		node.child[i].traverse(indent + 4)
	}
}

func main() {
	file, err := os.OpenFile("btree.dat", os.O_RDWR|os.O_CREATE, 0666)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	btree := &BTree{
		t:    3,
		file: file,
	}

	btree.insert(2)
	btree.insert(30)
	btree.insert(25)
	btree.insert(60)
	btree.insert(53)
	btree.insert(24)
	btree.insert(29)
	btree.insert(20)
	btree.insert(18)

	btree.delete(30)

	fmt.Println("szukanie klucza 15: ", btree.root.search(15))
	fmt.Println("szukanie klucza 60: ", btree.root.search(60))

	btree.printTree()

}
