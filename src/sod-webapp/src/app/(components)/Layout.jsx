import BackgroundImage from "./BackgroundImage";
import Card from "./Card";
import Navbar from "./Navbar";

export default function Layout({ children }) {
  return (
    <BackgroundImage>
      <Navbar />
      <Card>{children}</Card>
    </BackgroundImage>
  );
}
