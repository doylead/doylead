// components/Frame.tsx
import React from 'react';
import Link from 'next/link';
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter'; // Make sure you have gray-matter installed

interface FrameProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

const Frame: React.FC<FrameProps> = async ({ children, ...rest }) => {
  // Fetch blog post data (this should ideally be a separate function)
  const postsDirectory = path.join(process.cwd(), 'posts');
  const filenames = await fs.readdir(postsDirectory);

  const posts = await Promise.all(
    filenames
      .filter((filename) => filename.endsWith('.md'))
      .map(async (filename) => {
        const filePath = path.join(postsDirectory, filename);
        const fileContents = await fs.readFile(filePath, 'utf8');
        const { data } = matter(fileContents);
        return {
          slug: filename.replace(/\.md$/, ''),
          title: data.title as string,
          date: new Date(data.date)
        };
      })
  );
  
  posts.sort((a, b) => b.date.getDate() - a.date.getDate());

  return (
    <div className="flex flex-col min-h-screen" {...rest}>
      {/* Banner */}
      <div className="bg-[#40798C] p-4">
        {/* Banner content can go here */}
      </div>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="bg-[#70A9A1] w-64 shrink-0 p-4">
          <h2 className="text-xl font-bold mb-4 px-4 pt-4 pb-0">Blog Posts</h2>
          <ul className="px-12 list-disc">
            {posts.map((post) => (
              <li key={post.slug} className="mb-2">
                <Link href={`/posts/${post.slug}/`}>
                  {post.title}
                </Link>
              </li>
            ))}
          </ul>
        </aside>

        {/* Dynamic Content Area */}
        <main className="bg-[#F6F1D1] flex-1 p-4 overflow-y-auto">
          {children}
        </main>
      </div>
      {/* Banner */}
      <div className="bg-[#40798C] p-4">
        {/* Banner content can go here */}
      </div>
    </div>
  );
};

export default Frame;