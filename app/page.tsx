import { redirect } from "next/navigation";

export default async function Home() {
  // Because I don't have anything better to do on this page now
  redirect('posts/HelloWorld')
}