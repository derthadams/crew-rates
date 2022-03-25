import { useEffect, useRef, useState } from "react";

export default function useObserver( targetRef ) {
    const [isLoading, setIsLoading] = useState(false);
    const observerRef = useRef(null);

    const options = {
        threshold: 0
    }

    useEffect(() => {
        observerRef.current = new IntersectionObserver(([entry]) => {
            console.log(entry);
            setIsLoading(entry.isIntersecting);
            setTimeout(() => {
                setIsLoading(false)
            }, 500);
        }, options);
    }, []);

    useEffect(() => {
        console.log("targetRef", targetRef);
        observerRef.current.observe(targetRef.current);

        return () => {
            observerRef.current.disconnect();
        };
    }, [targetRef]);

    return isLoading;
}