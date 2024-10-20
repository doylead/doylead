import path from 'path';
import { readFile } from 'fs/promises';
import matter from 'gray-matter';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeHighlight from 'rehype-highlight'; 
import rehypeStringify from 'rehype-stringify';
import rehypeRewrite from 'rehype-rewrite';
import DOMPurify from 'isomorphic-dompurify';

// Create a data type for the markdown post including
// post metadata
export interface PostData {
  title: string;
  date: Date;
  content: string;
}

export async function getMarkdown(
    directoryName: string, 
    fileName: string
): Promise<PostData | null> {
  // Specify the markdown file to read
  const postsDirectory = path.join(process.cwd(), directoryName);
  const filePath = path.join(postsDirectory, `${fileName}.md`);

  try {
    const fileContents = await readFile(filePath, 'utf8');
    const { data, content } = matter(fileContents);

    // Specify classes to add to various markdown elements
    // for Tailwind CSS
    const classConfig: { [key: string]: string } = {
        h1: 'text-2xl font-bold underline pt-4',
        h2: 'text-xl font-semibold underline pt-4',
        h3: 'text-lg font-medium pt-4',
        ul: 'pl-8 list-disc',
        ol: 'pl-8 list-decimal',
        a: 'text-blue-600 underline',
        blockquote: 'bg-[#cfd7c7] px-8'
      };

    // Define a pipeline for parsing markdown files to
    // HTML, including adding Tailwind CSS
    const processedContent = await unified()
      .use(remarkParse)
      // Allows markdown to incorporate arbitrary HTML
      .use(remarkRehype, { allowDangerousHtml: true })
      .use(rehypeRaw)  
      .use(rehypeHighlight)  
      .use(rehypeRewrite, { 
        rewrite: (node) => {
          if (node.type !== 'element') return;
          if (classConfig[node.tagName]) {
            node.properties.className = classConfig[node.tagName]; 
          }
        }
      })
      .use(rehypeStringify)
      .process(content);

    let markdownHtml = processedContent.toString();

    // Sanitize the HTML to prevent XSS attacks
    markdownHtml = DOMPurify.sanitize(markdownHtml);

    return {
      title: data.title,
      date: new Date(data.date),
      content: markdownHtml, 
    };
  } catch (error) {
    console.error('Error getting post data:', error);
    return null;
  }
}
