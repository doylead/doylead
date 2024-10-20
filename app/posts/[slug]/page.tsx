import { notFound } from 'next/navigation';
import { getMarkdown } from "@/app/lib/utils";

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await getMarkdown("posts", params.slug);

  if (!post) {
    return notFound(); 
  }

  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold mb-2">{post.title}</h1>
      <p className="text-gray-600 mb-2">
        {
        // Currently dates read from Markdown files are assumed to be in UTC.  This prevents
        // conversion between UTC and local time zone, which yields more sensible results to
        // readers in the Eastern US.  To modify behavior on the read side, check app/lib/utils.ts
        }
        {post.date.toLocaleString(
          'en-us', {timeZone: "UTC", day: "2-digit", month: "short", year: "numeric"}
        )}
      </p>
      <article dangerouslySetInnerHTML={{ __html: post.content }} />
    </main>
  );
}