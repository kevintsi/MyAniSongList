import { useRouter } from 'next/router'

const Delete = () => {
    const router = useRouter()
    const { id } = router.query

    return <p>Delete Post: {id}</p>
}

export default Delete