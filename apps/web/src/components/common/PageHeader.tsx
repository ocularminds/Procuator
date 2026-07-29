interface PageHeaderProps {
  title: string;
  description: string;
}
export function PageHeader({ title, description }: PageHeaderProps) {
  return (
    <div className="mb-8">
      <h1 className="text-3xl font-semibold tracking-tight text-white">{title}</h1>
      <p className="mt-2 text-white/70">{description}</p>
    </div>
  );
}
